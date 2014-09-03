__author__ = 'guillermo'

from json import dumps


def success(data):
    return dumps({"success": True, "data": data})


def error(text=""):
    return dumps({"success": False, "error": text})


def uri(element, element_code, level, url_root=None):
    element["uri"] = "%s%s/%s" % (url_root, level, element[element_code])
