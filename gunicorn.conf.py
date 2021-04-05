import time
import json

import redis

# --------------------- Setup ---------------------
def when_ready_callback(server):
    network_info = None
    with open("network.json") as network_file:
        network_info = json.loads("".join([s.strip() for s in network_file.readlines()]))

    redis_client = redis.Redis(host=network_info["redis_addr"], port=network_info["redis_port"], password=network_info["redis_pass"])
    redis_client.set("is_compressing", 0)
    redis_client.set("num_compressions", 0, nx=True)


time_str = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())

# --------------------- Actual Config ---------------------
when_ready = when_ready_callback

accesslog = "gunicorn_log/{}_gunicorn.access.log".format(time_str)
errorlog = "gunicorn_log/{}_gunicorn.log".format(time_str)
loglevel = "info"
capture_output = True

worker_class = "gevent"
workers = 6
threads = 8

bind = ["127.0.0.1:5000"]