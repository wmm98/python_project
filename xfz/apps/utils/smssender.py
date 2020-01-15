import requests


def send(mobile, captcha):
    # print("执行send函数+++++++++++++++++++")
    url = "http://v.juhe.cn/sms/send"
    params = {
        "mobile": mobile,
        "tpl_id": "206189",  # 您申请的短信模板ID，根据实际情况修改
        "tpl_value": "#code#=" + captcha,  # 您设置的模板变量，根据实际情况修改
        "key": "f2f06fc94acab5c6d049c57fa48cc51f",  # 应用APPKEY(应用详细页查询)

    }

    response = requests.get(url, params=params)
    result = response.json()
    # print("==================")
    # print(result)
    if result['error_code'] == 0:
        return True
    else:
        return False

# def send(mobile,captcha):
#     url = "http://v.juhe.cn/sms/send"
#     params = {
#         "mobile": mobile,
#         "tpl_id": "121674",
#         "tpl_value": "#code#="+captcha,
#         "key": "4f2dc49ce16b8538522f0f11fb6cd0a2"
#     }
#     response = requests.get(url, params=params)
#     result = response.json()
#     if result['error_code'] == 0:
#         return True
#     else:
#         return False
