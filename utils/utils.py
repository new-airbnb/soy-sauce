from datetime import datetime


def get_timestamp(t=None):
    dt = t if t else datetime.utcnow()
    return dt.isoformat() + 'Z'
