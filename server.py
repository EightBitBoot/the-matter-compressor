import os
from flask import Flask
from flask import request, jsonify
from threading import Thread, Lock

class EncodingState:
    def __init__(self) -> None:
        self._is_encoding = False # DO NOT ACCESS THIS WITHOUT USING THE LOCK
        self._encoding_lock = Lock()

    def is_encoding(self) -> bool:
        result = True # A false negative is more harmful than a false positive

        self._encoding_lock.acquire()
        result = self._is_encoding
        self._encoding_lock.release()

        return result

    def set_state(self, new_state: bool) -> None:
        self._encoding_lock.acquire()
        self._is_encoding = new_state
        self._encoding_lock.release()


app = Flask("TheEncoder")
encoding_state = EncodingState()

def perform_encode():
    global encoding_state

    encoding_state.set_state(True)

    os.system("sleep {}".format(20))
    print("Done encoding")

    encoding_state.set_state(False)


def start_encode():
    encode_thread = Thread(target=perform_encode)
    encode_thread.setName("EncodingThread")
    encode_thread.setDaemon(True)
    encode_thread.start()


@app.route("/", methods=["GET"])
def index_route():
    return "Oh hai mark!"


@app.route("/encode", methods=["GET", "POST"])
def encode_route():
    result = {}

    if request.method == "GET":
        result = {"encoding": encoding_state.is_encoding()}

    if request.method == "POST":
        result = {"success": False}

        if not encoding_state.is_encoding():
            start_encode()
            result["success"] = True
        else:
            result["success"] = False

    return jsonify(result)