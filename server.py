from gevent import monkey
monkey.patch_all() # Patch blocking functions

import os
import time
import json
import random
import subprocess
from threading import Thread

from flask import Flask, url_for
from flask import request, jsonify

from celery import Celery

from flask_sse import sse

import redis
import redlock

CRF_MIN = 29
CRF_MAX = 31

class CompressionState:
    def __init__(self, redis_url) -> None:
        self._redis_client = redis.from_url(redis_url)
        lock_factory = redlock.RedLockFactory([self._redis_client])
        self._num_compressions_lock = lock_factory.create_lock("num_compressions_lock")
        self._is_compressing_lock = lock_factory.create_lock("is_compressing_lock")

    def _perform_action_in_lock(self, lock, action): 
        lock_success = lock.acquire()
        while not lock_success:
            time.sleep(random.randint(1, 5) / 1000)
            lock_success = lock.acquire()

        result = action()

        lock.release() 

        return result

    def is_compressing(self) -> bool:
        raw_result = self._perform_action_in_lock(self._is_compressing_lock, lambda: self._redis_client.get("is_compressing"))

        return bool(int(raw_result))

    def set_is_compressing(self, new_state: bool) -> None:
        self._perform_action_in_lock(self._is_compressing_lock, lambda: self._redis_client.set("is_compressing", int(new_state)))

    def get_num_compressions(self) -> int:
        result = self._perform_action_in_lock(self._num_compressions_lock, lambda: self._redis_client.get("num_compressions"))

        return int(result)
        
    def increment_num_compressions(self) -> None:
        self._perform_action_in_lock(self._num_compressions_lock, lambda: self._redis_client.incr("num_compressions"))


def make_celery(app):
    celery = Celery(app.import_name, backend=app.config["result_backend"], broker=app.config["CELERY_BROKER_URL"])
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


# --------------- INITIALIZATION CODE --------------- 
# Not sure a better place to put this with flask
app = Flask("TheMatterCompressor")

network_info = None
with open("network.json") as network_file:
    network_info = json.loads("".join([s.strip() for s in network_file.readlines()]))

app.config["REDIS_URL"] = "redis://:{}@{}:{}".format(network_info["redis_pass"], network_info["redis_addr"], network_info["redis_port"]) # For flask-sse
compression_state = CompressionState(app.config["REDIS_URL"])

app.config.update(CELERY_BROKER_URL=app.config["REDIS_URL"], result_backend=app.config["REDIS_URL"])
celery = make_celery(app)

app.register_blueprint(sse, url_prefix="/events")


@celery.task
def publish_keep_alive():
    sse.publish({"message": "keep_alive"}, type="keep_alive")
    print("Sent keep_alive")

celery.conf.beat_schedule = {
    "keep-alive-every-30-seconds": {
        "task": "server.publish_keep_alive",
        "schedule": 30.0,
        "args": None
    },
}


@celery.task
def perform_compression():
    global compression_state

    random.seed(time.time())
    crf = random.randint(CRF_MIN, CRF_MAX)

    compression_state.set_is_compressing(True)
    print("[{}] Starting compression: CRF {}".format(time.ctime(), crf))
    with app.app_context():
        sse.publish({"message": "oh hello mario"}, type="compress")

    subprocess.run(["bash", "-c", "./compress.sh {} {}".format(compression_state.get_num_compressions(), crf)])

    print("[{}] Done compressing".format(time.ctime()))
    compression_state.set_is_compressing(False)
    compression_state.increment_num_compressions()

    with app.app_context():
        sse.publish({"message": "oh goodbye mario"}, type="compress")


def start_compression():
    compress_thread = Thread(target=perform_compression)
    compress_thread.setName("CompressionThread")
    compress_thread.setDaemon(True)
    compress_thread.start()


@app.route("/", methods=["GET"])
def index_route():
    with open("index.html") as index_file:
        return "\n".join(index_file.readlines())


@app.route("/compress", methods=["GET", "POST"])
def compress_route():
    result = {"num_compressions": compression_state.get_num_compressions()}

    if request.method == "GET":
        result["is_compressing"] = compression_state.is_compressing()

    if request.method == "POST":
        result = {"success": False}

        if not compression_state.is_compressing():
            perform_compression.delay()
            result["success"] = True
        else:
            result["success"] = False

    return jsonify(result)