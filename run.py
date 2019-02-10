import sys

from flask import Flask

from utils import config

app = Flask(__name__)


def app_init():
    pass


@app.route("/ping", methods=["GET"])
def ping():
    return "pong!"


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Error: Missing config file, try again with your config file.")
        exit(0)

    config.init(sys.argv[1])
    host, port, debug = config.conf["host"], config.conf["port"], config.conf["debug"]
    app_init()
    app.run(host, port, debug)
