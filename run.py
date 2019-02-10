import sys

from new_airbnb import app
from utils import config


def app_init():
    if len(sys.argv) == 1:
        print("Error: Missing config file, try again with your config file.")
        exit(0)

    config.init(sys.argv[1])
    host, port, debug = config.conf["host"], config.conf["port"], config.conf["debug"]

    import views
    app.run(host, port, debug)


if __name__ == "__main__":
    app_init()
