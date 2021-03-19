from flask import Flask
from flask import request

app = Flask("TheEncoder")


@app.route("/", methods=["GET"])
def hello_world():
    return "Hello world!"

@app.route("/encode", methods=["GET", "POST"])
def encode():
    if request.method == "GET":
        pass

    if request.method == "POST":
        pass