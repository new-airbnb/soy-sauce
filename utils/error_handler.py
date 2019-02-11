import logging

from flask import jsonify

from utils import error_msg

logger = logging.getLogger(__name__)


def handler(code, msg, error):
    error_info = {
        'default': 1,
        'error': '{}:{}'.format(type(error), str(error))
    }
    logger.error('Default error handler {}, {}'.format(code, error_info['error']))
    return jsonify({
        'success': 0,
        'msg': msg,
        '_error_info': error_info  # for diagnosis
    }), code


def generate(app, ec):
    app.register_error_handler(
        ec,
        lambda error: handler(ec, getattr(error_msg, 'MSG_{}'.format(ec)), error)
    )
