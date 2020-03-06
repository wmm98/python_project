# encoding: utf-8
from django.shortcuts import render
from .models import Course, CourseOrder
import time, hmac, os, hashlib
from django.conf import settings
from ..utils import restful
from apps.xfzauth.decorators import xfz_login_required
from hashlib import md5
from django.shortcuts import reverse
from django.views.decorators.csrf import csrf_exempt


def course_index(request):
    context = {
        'courses': Course.objects.all()
    }
    return render(request, 'course/course_index.html', context=context)


def course_detail(request, course_id):
    course = Course.objects.get(pk=course_id)
    buyed = CourseOrder.objects.filter(course=course, buyer=request.user, status=2).exists()
    context = {
        'course': course,
        'buyed': buyed
    }
    return render(request, 'course/course_detail.html', context=context)


# 代码修改过与讲师的不一样
def course_token(request):
    # video：是视频文件的完整链接
    file = request.GET.get('video')

    course_id = request.GET.get('course_id')

    if CourseOrder.objects.filter(course_id=course_id, buyer=request.user, status=2).exists() \
            or Course.objects.filter(pk=course_id, price=0).exists():
        expiration_time = int(time.time()) + 2 * 60 * 60

        USER_ID = settings.BAIDU_CLOUD_USER_ID
        USER_KEY = settings.BAIDU_CLOUD_USER_KEY

        # file=http://hemvpc6ui1kef2g0dd2.exp.bcevod.com/mda-igjsr8g7z7zqwnav/mda-igjsr8g7z7zqwnav.m3u8
        extension = os.path.splitext(file)[1]
        media_id = file.split('/')[-1].replace(extension, '')

        # unicode->bytes=unicode.encode('utf-8')bytes
        key = USER_KEY.encode('utf-8')
        message = '/{0}/{1}'.format(media_id, expiration_time).encode('utf-8')
        signature = hmac.new(key, message, digestmod=hashlib.sha256).hexdigest()
        token = '{0}_{1}_{2}'.format(signature, USER_ID, expiration_time)
        return restful.result(data={'token': token})

    else:
        return restful.params_error(message='请先购买课程！')


# notify_url = ''


@xfz_login_required
def course_order(request, course_id):
    course = Course.objects.get(pk=course_id)
    order = CourseOrder.objects.create(course=course, buyer=request.user, status=1, amount=course.price)
    # print("================测试============================")
    # notify_url = request.build_absolute_uri(reverse('course:notify_view'))
    # print("============================================================")
    context = {
        'goods': {
            'thumbnail': course.cover_url,
            'title': course.title,
            'price': course.price
        },
        'order': order,
        # /course/notify_url/
        'notify_url': request.build_absolute_uri(reverse('course:notify_view')),
        'return_url': request.build_absolute_uri(reverse('course:course_detail', kwargs={"course_id": course.pk}))
    }
    return render(request, 'course/course_order.html', context=context)


@xfz_login_required
def course_order_key(request):
    goodsname = request.POST.get("goodsname")
    istype = request.POST.get("istype")
    notify_url = request.POST.get("notify_url")
    orderid = request.POST.get("orderid")
    price = request.POST.get("price")
    return_url = request.POST.get("return_url")

    token = 'e712ca6aa42287ea29a4f44173d478e1'
    uid = 'ef947fef59ae583e978892c1'
    orderuid = str(request.user.pk)

    print('goodsname:', goodsname)
    print('istype:', istype)
    print('notify_url:', notify_url)
    print('orderid:', orderid)
    print('price:', price)
    print('return_url:', return_url)

    key = md5((goodsname + istype + notify_url + orderid + orderuid + price + return_url + token + uid).encode(
        "utf-8")).hexdigest()
    return restful.result(data={"key": key})


@csrf_exempt
def notify_view(request):
    print("-------------------------------")
    orderid = request.POST.get('orderid')
    # orderid = notify_url
    print("--------------------------------")
    print('=' * 10)
    print(orderid)
    print('=' * 10)
    # 大于0
    # if CourseOrder.objects.filter(pk=orderid, status=1, buyer=request.user):
    CourseOrder.objects.filter(pk=orderid).update(status=2)
    # print("========================")
    return restful.ok()
