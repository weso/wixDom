__author__ = 'guillermo'

def success(data):
    return {"success": True, "data": data}

def error(text=""):
    return {"success": False, "error": text}

def uri(element, element_code, level, url_root=None):
    element["uri"] = "%s%s/%s" % (url_root, level, element[element_code])
