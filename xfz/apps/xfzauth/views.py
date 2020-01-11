from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login, logout, authenticate
from django.views.decorators.http import require_POST
from .forms import LoginForm
from django.http import JsonResponse
from ..utils import restful


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
