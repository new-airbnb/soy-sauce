import logging

from django.http import JsonResponse

from utils import error_msg

logger = logging.getLogger(__name__)

def handler(code, msg, kwargs):
    error_info = {
        'default': 1,
        'error': str(kwargs)
    }
    logger.error('Default error handler {}:{}'.format(code, error_info['error']))
    return JsonResponse({
        'success': 0,
        'msg': msg,
        '_error_info': error_info  # for diagnosis
    }, status=code)
