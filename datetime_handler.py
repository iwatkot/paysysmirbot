from datetime import datetime


def get_today():
    return str(datetime.now())[:10]


def get_now():
    return str(datetime.now()).replace(' ', '--')[:17]
