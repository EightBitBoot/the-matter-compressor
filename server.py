import os
import time
import random
import subprocess
from threading import Thread, Lock

from flask import Flask
from flask import request, jsonify

CRF_MIN = 29
CRF_MAX = 31

class CompressionState:
    def __init__(self) -> None:
        self._is_compressing        = False  # DO NOT ACCESS THIS WITHOUT USING THE LOCK
        self._is_compressing_lock   = Lock()
        self._num_compressions      = 0      # DO NOT ACCESS THIS WITHOUT USING THE LOCK
        self._num_compressions_lock = Lock()

    def is_compressing(self) -> bool:
        result = True # A false negative is more harmful than a false positive

        self._is_compressing_lock.acquire()
        result = self._is_compressing
        self._is_compressing_lock.release()

        return result

    def set_is_compressing(self, new_state: bool) -> None:
        self._is_compressing_lock.acquire()
        self._is_compressing = new_state
        self._is_compressing_lock.release()

        if new_state == True: # For clarity
            # is_compressing is changing from false to true marking a new round
            # of compression: increment the number of compressions
            self._num_compressions_lock.acquire()
            self._num_compressions += 1
            self._num_compressions_lock.release()

    def get_num_compressions(self) -> int:
        result = 0

        self._num_compressions_lock.acquire()
        result = self._num_compressions
        self._num_compressions_lock.release()

        return result


app = Flask("TheMatterCompressor")
compression_state = CompressionState()

def perform_compression():
    global compression_state

    random.seed(time.time())
    crf = random.randint(CRF_MIN, CRF_MAX)

    compression_state.set_is_compressing(True)
    print("[{}] Starting compression: CRF {}".format(time.ctime(), crf))

    subprocess.run(["bash", "-c", "./compress.sh {} {}".format(compression_state.get_num_compressions(), crf)])

    print("[{}] Done compressing".format(time.ctime()))
    compression_state.set_is_compressing(False)


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
            start_compression()
            result["success"] = True
        else:
            result["success"] = False

    return jsonify(result)