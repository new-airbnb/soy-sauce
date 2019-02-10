import json
import logging

conf = {
    "log_level": "INFO",
    "host": "0.0.0.0",
    "port": 8080,
    "debug": True,
    "database_uri": "",
    "database_name": "",
    "sentry_dsn": ""
}

log_level_list = ["CRITICAL", "FATAL", "DEBUG", "INFO", "WARNING", "WARN", "ERROR", "NOTSET"]


def init(config_file):
    with open(config_file) as f:
        _conf = json.load(f)
        for k, v in _conf.items():
            if k in conf:
                conf[k] = v
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
                        format="%(asctime)s - %(name)s - %(levelname)s - %(lineno)d - %(module)s - %(message)s",
                        )
