import json
import logging
import os

from db.dbutils import connect_db

conf = {
    "log_level": "INFO",
    "host": "0.0.0.0",
    "port": os.environ.get("PORT", 9991),
    "debug": True,
    "database_uri": "",
    "sentry_dsn": ""
}

log_level_list = ["CRITICAL", "FATAL", "DEBUG", "INFO", "WARNING", "WARN", "ERROR", "NOTSET"]


def init(config_file):
    """initialize the config file"""
    with open(config_file) as f:
        _conf = json.load(f)
        for k, v in _conf.items():
            if k in conf:
                conf[k] = v

    if conf["database_uri"] != "":
        connect_db(conf["database_uri"])
    else:
        print("Error: Missing \"database_uri\" in config file.")
        exit(0)

    if conf["log_level"].upper() not in log_level_list:
        print("Unknown logging level in config: {}. Will use INFO".format(conf["log_level"]))
        level = logging.INFO
    else:
        level = conf["log_level"]

    log_init(level)

    if conf["sentry_dsn"] != "":
        import sentry_sdk
        from sentry_sdk.integrations.flask import FlaskIntegration
        sentry_sdk.init(conf["sentry_dsn"],
                        integrations=[FlaskIntegration()])
    else:
        logging.info("Not Found Sentry DSN in config file")


def log_init(level):
    logging.basicConfig(level=level,
                        datefmt="%Y/%m/%d %H:%M:%S",
                        format="%(asctime)s - %(name)s:%(lineno)d - %(module)s - %(levelname)s - %(message)s",
                        )
