import json
import logging
import os

conf = {
    "log_level": "INFO",
    "database_uri": os.environ.get("DATABASE_URI", ""),
    "database_name": os.environ.get("DATABASE_NAME", ""),
    "sentry_dsn": os.environ.get("SENTRY_DSN", ""),
    "house_location_collection": os.environ.get("HOUSE_LOCATION_COLLECTION", ""),
    "test_database_uri": os.environ.get("TEST_DATABASE_URI", ""),
    "test_database_name": os.environ.get("TEST_DATABASE_NAME", ""),
}

log_level_list = ["CRITICAL", "FATAL", "DEBUG", "INFO", "WARNING", "WARN", "ERROR", "NOTSET"]


def init(config_file):
    """initialize the config file"""
    with open(config_file) as f:
        _conf = json.load(f)
        for k, v in _conf.items():
            if k in conf:
                conf[k] = v

    if conf["database_uri"] == "":
        print("Error: Missing \"database_uri\" in config file.")
        exit(0)

    if conf["log_level"].upper() not in log_level_list:
        print("Unknown logging level in config: {}. Will use INFO".format(conf["log_level"]))
        conf["log_level"] = 'INFO'

    if conf["sentry_dsn"] != "":
        import sentry_sdk
        from sentry_sdk.integrations.django import DjangoIntegration
        sentry_sdk.init(conf["sentry_dsn"],
                        integrations=[DjangoIntegration()])
    else:
        logging.info("Not Found Sentry DSN in config file")


init('config.json')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,  # keep Django's default loggers
    'formatters': {
        'standard': {
            'format': '%(asctime)s - %(name)s:%(lineno)d - %(module)s - %(levelname)s - %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',  # this level or higher goes to the console
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
    },
    'loggers': {
        'django': {  # configure all of Django's loggers
            'handlers': ['console'],
            'level': 'INFO',  # this level or higher goes to the console
            'propagate': False,  # don't propagate further, to avoid duplication
        },
        'djongo': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        # root configuration – for all of our own apps
        '': {
            'handlers': ['console'],
            'level': conf['log_level'],  # this level or higher goes to the console,
        },
    },
}
