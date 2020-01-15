from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login, logout, authenticate
from django.views.decorators.http import require_POST
from .forms import LoginForm, RegisterForm
from django.http import JsonResponse, HttpResponse
from ..utils import restful, smssender
from ..utils.captcha.xfzcaptcha import Captcha
from io import BytesIO
from django.core.cache import cache
from django.contrib.auth import get_user_model
User = get_user_model()


# 传给前端的数据设置
# {"code": 400, "message": "", "data": {}}

# 前端提交的数据
@require_POST
def login_view(request):
    form = LoginForm(request.POST)
    # 表单验证成功
    if form.is_valid():
        # 获取数据
        telephone = form.cleaned_data.get("telephone")
        password = form.cleaned_data.get("password")
        remember = form.cleaned_data.get("remember")
        # 用户验证
        user = authenticate(request, username=telephone, password=password)
        # 用户存在
        if user:
            # 不是黑名单
            if user.is_active:
                # 登录
                login(request, user)
                if remember:
                    # 默认两周后过期
                    request.session.set_expiry(None)
                else:
                    # 关闭浏览器的时候过期
                    request.session.set_expiry(0)
                return restful.ok()
            # 黑名单的人
            else:
                return restful.unauth(message="您的账号已经被冻结")
        # 用户不存在
        else:
            return restful.params_error(message="手机号码或密码错误")
    # 表单验证失败
    else:
        # 错误信息
        errors = form.get_errors()
        return restful.params_error(message=errors)


# 退出登录
def logout_view(request):
    logout(request)
    return redirect(reverse('index'))


# 注册页面
@require_POST
def register(request):
    form = RegisterForm(request.POST)
    if form.is_valid():
        telephone = form.cleaned_data.get("telephone")
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")
        user = User.objects.create_user(telephone=telephone, username=username, password=password)
        login(request, user)
        return restful.ok()
    else:
        return restful.params_error(message=form.get_errors())


# 图形验证码
def img_captcha(request):
    # 接收返回的imag和text
    text, image = Captcha.gene_code()
    # print(text)
    # BytesIO:相当于一个管道，用于存储图片的流数据
    out = BytesIO()
    # 调用sava方法， 将这个img对象保存到BytesIO中
    image.save(out, 'png')
    # 将文件指针BytesIO移动到最开始的位置
    out.seek(0)
    response = HttpResponse(content_type="image/png")
    # 从BytesIO的管道中，读取出图片的数据，保存到response对象上
    response.write(out.read())
    response["Content-length"] = out.tell()
    # 储存验证码, 3分钟过期
    cache.set(text.lower(), text.lower(), 5*60)
    return response


# 短信验证码
def sms_captcha(request):
    # /sms_captcha/?telephone=xxx
    telephone = request.GET.get('telephone')
    print(telephone)
    # 从restful中调用随机生成的验证码
    # code = Captcha.gene_number()
    # 测试代码
    code = Captcha.gene_text()
    # 三分钟过期，储存验证码
    cache.set(telephone, code, 5 * 60)
    print("短信验证码：", code)
    result = smssender.send(telephone, code)
    print(result)
    if result:
        return restful.ok()
    else:
        return restful.params_error(message="短信验证码发送失败！")


# 测试cacahe
def cache_test(request):
    cache.set('username', 'zhiliao', 60)
    result = cache.get('username')
    print(result)
    return HttpResponse('success')
