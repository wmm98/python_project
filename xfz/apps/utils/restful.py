from django.http import JsonResponse


class HttpCode(object):
    ok = 200
    # 参数错误
    paramserror = 400
    # 没有权限
    unauth = 401
    # 方法错误
    methoderror = 405
    # 浏览器出错
    servererror = 500


# {"code": 200, "message": "", "data": {}} 默认得参数
def result(code=HttpCode.ok, message="", data=None, kwargs=None):
    json_dict = {"code": code, "message": message, "data": data}

    # 有传进其他的而参数而且这个参数是字典并且有值：
    if kwargs and isinstance(kwargs, dict) and kwargs.keys():
        # 更新数据
        json_dict.update(kwargs)

    return JsonResponse(json_dict)


def ok():
    return result()


def params_error(message="", data=None):
    return result(code=HttpCode.paramserror, message=message, data=data)


def unauth(message="", data=None):
    return result(code=HttpCode.unauth, message=message, data=data)


def method_error(message="", data=None):
    return result(code=HttpCode.methoderror, message=message, data=data)


def server_error(message="", data=None):
    return result(code=HttpCode.servererror, message=message, data=data)