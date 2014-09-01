__author__ = 'guillermo'

from json import dumps


def success(data):
    return dumps({"success": True, "data": data})


def error(text=""):
    return dumps({"success": False, "error": text})
