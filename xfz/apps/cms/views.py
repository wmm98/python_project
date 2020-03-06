from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic import View
from django.views.decorators.http import require_POST, require_GET
from ..news.models import NewsCategory, News, Banner
from ..course.models import Course, CourseCategory
from ..payinfo.models import Payinfo, PayinfoOrder
from ..utils import restful
from .forms import EditNewsCategoryForm, WriteNewsForm, AddBannerForm, EditBannerForm, EditNewsForm, PubCourseForm, \
    PayInfoForm
import os
from django.conf import settings
import qiniu
from ..news.serializers import BannerSerializer
from datetime import datetime
from django.utils.timezone import make_aware
from django.core.paginator import Paginator
from urllib import parse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required


# 发布资讯
@method_decorator(permission_required(perm="payinfo.add_payinfo", login_url='/'), name='dispatch')
class PayInfoView(View):
    def get(self, request):
        payinfo = Payinfo.objects.all()
        context = {
            'payinfo': payinfo
        }
        return render(request, 'cms/pay_info.html', context=context)

    def post(self, request):
        title = request.POST.get("title")
        profile = request.POST.get("profile")
        path = request.POST.get("path")
        price = request.POST.get("price")

        print("=========================")
        # form = PayInfoForm(request.POST)
        # if form.is_valid():
        # title = form.cleaned_data.get("title")
        print(title)
        # profile = form.cleaned_data.get("profile")
        print(profile)

        # path = form.cleaned_data.get("path")
        print(path)
        print("===========path============")
        # price = form.cleaned_data.get("price")
        Payinfo.objects.create(title=title, profile=profile, path=path, price=price)
        return restful.ok()
        # else:
        #     Payinfo.objects.create(title=title, profile=profile, path=path, price=price)
        #     return restful.ok()

        # return restful.params_error(message=form.get_errors())


@method_decorator(permission_required(perm="payinfo.change_payinfo", login_url='/'), name='dispatch')
class PayInfoListView(View):
    def get(self, request):
        # request.GET：获取出来的所有数据，都是字符串类型
        page = int(request.GET.get('p', 1))
        title = request.GET.get('title')
        profile = request.GET.get('profile')
        # request.GET.get(参数,默认值)
        # 这个默认值是只有这个参数没有传递的时候才会使用
        # 如果传递了，但是是一个空的字符串，那么也不会使用默认值

        payinfoes = Payinfo.objects.all()

        if title:
            payinfoes = payinfoes.filter(title__icontains=title)

        if profile:
            payinfoes = payinfoes.filter(profile__icontains=profile)

        paginator = Paginator(payinfoes, 4)
        page_obj = paginator.page(page)

        context_data = self.get_pagination_data(paginator, page_obj)

        context = {
            'payinfoes': page_obj.object_list,
            'page_obj': page_obj,
            'paginator': paginator,

            'title': title,
            'profile': profile,

            'url_query': '&' + parse.urlencode({

                'profile': profile or '',
                'title': title or '',

            })
        }

        context.update(context_data)
        return render(request, 'cms/payinfo_list.html', context=context)

    def get_pagination_data(self, paginator, page_obj, around_count=2):
        current_page = page_obj.number
        num_pages = paginator.num_pages

        left_has_more = False
        right_has_more = False

        if current_page <= around_count + 2:
            left_pages = range(1, current_page)
        else:
            left_has_more = True
            left_pages = range(current_page - around_count, current_page)

        if current_page >= num_pages - around_count - 1:
            right_pages = range(current_page + 1, num_pages + 1)
        else:
            right_has_more = True
            right_pages = range(current_page + 1, current_page + around_count + 1)

        return {
            # left_pages：代表的是当前这页的左边的页的页码
            'left_pages': left_pages,
            # right_pages：代表的是当前这页的右边的页的页码
            'right_pages': right_pages,
            'current_page': current_page,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'num_pages': num_pages
        }


@method_decorator(permission_required(perm="payinfo.change_payinfo", login_url='/'), name='dispatch')
class EditPayInfoView(View):
    def get(self, request):
        payinfo_id = request.GET.get('payinfo_id')
        payinfo = Payinfo.objects.get(pk=payinfo_id)
        context = {
            'payinfo': payinfo,
        }
        return render(request, 'cms/pay_info.html', context=context)

    def post(self, request):
        title = request.POST.get("title")
        profile = request.POST.get("profile")
        path = request.POST.get("path")
        price = request.POST.get("price")
        pk = request.POST.get("pk")

        Payinfo.objects.filter(pk=pk).update(title=title, profile=profile, path=path, price=price)
        return restful.ok()


@require_POST
@permission_required(perm="payinfo.delete_payinfo", login_url='/')
def delete_payinfo(request):
    payinfo_id = request.POST.get('payinfo_id')
    Payinfo.objects.filter(pk=payinfo_id).delete()
    return restful.ok()


# 没有访问权力的直接重定向到首页
@staff_member_required(login_url="index")
def index(request):
    return render(request, 'cms/index.html')


# 发布新闻页面
@method_decorator(permission_required(perm="news.add_news", login_url='/'), name='dispatch')
class WriteNewsView(View):
    def get(self, request):
        categories = NewsCategory.objects.all()
        context = {
            'categories': categories
        }
        return render(request, 'cms/write_news.html', context=context)

    def post(self, request):
        form = WriteNewsForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get("title")
            desc = form.cleaned_data.get("desc")
            thumbnail = form.cleaned_data.get("thumbnail")
            content = form.cleaned_data.get("content")
            category_id = form.cleaned_data.get("category")
            category = NewsCategory.objects.get(pk=category_id)
            News.objects.create(title=title, desc=desc, thumbnail=thumbnail, content=content, category=category,
                                author=request.user)
            return restful.ok()
        else:
            return restful.params_error(message=form.get_errors())


# 新闻分类
@require_GET
@permission_required(perm="news.add_newscategory", login_url='/')
def news_category(request):
    categories = NewsCategory.objects.all()
    context = {
        'categories': categories
    }
    return render(request, 'cms/news_category.html', context=context)


# 添加新闻分类
@require_POST
@permission_required(perm="news.add_newscategory", login_url='/')
def add_news_category(request):
    name = request.POST.get("name")
    # 判断分类是否存在
    exists = NewsCategory.objects.filter(name=name).exists()
    if not exists:
        # 添加
        NewsCategory.objects.create(name=name)
        return restful.ok()
    else:
        return restful.params_error(message="该分类已经存在！")


# 编辑新闻分类
@require_POST
@permission_required(perm="news.change_newscategory", login_url='/')
def edit_news_category(request):
    form = EditNewsCategoryForm(request.POST)
    if form.is_valid():
        pk = form.cleaned_data.get("pk")
        name = form.cleaned_data.get("name")
        try:
            NewsCategory.objects.filter(pk=pk).update(name=name)
            return restful.ok()
        except:
            return restful.params_error(message="该分类不存在")
    else:
        return restful.params_error(message=form.get_error())


# 删除分类
@require_POST
@permission_required(perm="news.delete_newscategory", login_url='/')
def delete_news_category(request):
    pk = request.POST.get("pk")
    try:
        NewsCategory.objects.filter(pk=pk).delete()
        return restful.ok()
    except:
        return restful.unauth(message='该分类不存在！')


# 上传图片
@require_POST
@staff_member_required(login_url='index')
def upload_file(request):
    file = request.FILES.get('file')
    name = file.name
    with open(os.path.join(settings.MEDIA_ROOT, name), 'wb') as fp:
        for chunk in file.chunks():
            fp.write(chunk)
    url = request.build_absolute_uri(settings.MEDIA_URL + name)
    # http://127.0.0.1:8000/media/abc.jpg
    return restful.result(data={'url': url})


@require_GET
@staff_member_required(login_url='index')
def qntoken(request):
    access_key = settings.QINIU_ACCESS_KEY
    secret_key = settings.QINIU_SECRET_KEY

    bucket = settings.QINIU_BUCKET_NAME
    q = qiniu.Auth(access_key, secret_key)
    token = q.upload_token(bucket)
    return restful.result(data={"token": token})


@permission_required(perm="news.add_banner", login_url='/')
def banners(request):
    return render(request, 'cms/banners.html')


@permission_required(perm="news.add_banner", login_url='/')
def add_banner(request):
    form = AddBannerForm(request.POST)
    if form.is_valid():
        priority = form.cleaned_data.get('priority')
        image_url = form.cleaned_data.get('image_url')
        link_to = form.cleaned_data.get('link_to')
        banner = Banner.objects.create(priority=priority, image_url=image_url, link_to=link_to)
        return restful.result(data={"banner_id": banner.pk})
    else:
        return restful.params_error(message=form.get_errors())


@permission_required(perm="news.add_banner", login_url='/')
def banner_list(request):
    banners = Banner.objects.all()
    serialize = BannerSerializer(banners, many=True)
    return restful.result(data=serialize.data)


@permission_required(perm="news.delete_banner",login_url='/')
def delete_banner(request):
    banner_id = request.POST.get('banner_id')
    Banner.objects.filter(pk=banner_id).delete()
    return restful.ok()


@permission_required(perm="news.change_banner",login_url='/')
def edit_banner(request):
    form = EditBannerForm(request.POST)
    if form.is_valid():
        pk = form.cleaned_data.get('pk')
        priority = form.cleaned_data.get('priority')
        image_url = form.cleaned_data.get('image_url')
        link_to = form.cleaned_data.get('link_to')
        Banner.objects.filter(pk=pk).update(image_url=image_url, link_to=link_to, priority=priority)
        return restful.ok()
    else:
        return restful.params_error(message=form.get_errors())


@method_decorator(permission_required(perm="news.change_news", login_url='/'), name='dispatch')
class NewsListView(View):
    def get(self, request):
        # request.GET：获取出来的所有数据，都是字符串类型
        page = int(request.GET.get('p', 1))
        start = request.GET.get('start')
        end = request.GET.get('end')
        title = request.GET.get('title')
        # request.GET.get(参数,默认值)
        # 这个默认值是只有这个参数没有传递的时候才会使用
        # 如果传递了，但是是一个空的字符串，那么也不会使用默认值
        category_id = int(request.GET.get('category', 0) or 0)

        newses = News.objects.select_related('category', 'author')

        if start or end:
            if start:
                start_date = datetime.strptime(start, '%Y/%m/%d')
            else:
                start_date = datetime(year=2018, month=6, day=1)
            if end:
                end_date = datetime.strptime(end, '%Y/%m/%d')
            else:
                end_date = datetime.today()
            newses = newses.filter(pub_time__range=(make_aware(start_date), make_aware(end_date)))

        if title:
            newses = newses.filter(title__icontains=title)

        if category_id:
            newses = newses.filter(category=category_id)

        paginator = Paginator(newses, 4)
        page_obj = paginator.page(page)

        context_data = self.get_pagination_data(paginator, page_obj)

        context = {
            'categories': NewsCategory.objects.all(),
            'newses': page_obj.object_list,
            'page_obj': page_obj,
            'paginator': paginator,
            'start': start,
            'end': end,
            'title': title,
            'category_id': category_id,
            'url_query': '&' + parse.urlencode({
                'start': start or '',
                'end': end or '',
                'title': title or '',
                'category': category_id or ''
            })
        }

        context.update(context_data)
        return render(request, 'cms/news_list.html', context=context)

    def get_pagination_data(self, paginator, page_obj, around_count=2):
        current_page = page_obj.number
        num_pages = paginator.num_pages

        left_has_more = False
        right_has_more = False

        if current_page <= around_count + 2:
            left_pages = range(1, current_page)
        else:
            left_has_more = True
            left_pages = range(current_page - around_count, current_page)

        if current_page >= num_pages - around_count - 1:
            right_pages = range(current_page + 1, num_pages + 1)
        else:
            right_has_more = True
            right_pages = range(current_page + 1, current_page + around_count + 1)

        return {
            # left_pages：代表的是当前这页的左边的页的页码
            'left_pages': left_pages,
            # right_pages：代表的是当前这页的右边的页的页码
            'right_pages': right_pages,
            'current_page': current_page,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'num_pages': num_pages
        }


@method_decorator(permission_required(perm="news.change_news", login_url='/'), name='dispatch')
class EditNewsView(View):
    def get(self, request):
        news_id = request.GET.get('news_id')
        news = News.objects.get(pk=news_id)
        context = {
            'news': news,
            'categories': NewsCategory.objects.all()
        }
        return render(request, 'cms/write_news.html', context=context)

    def post(self, request):
        form = EditNewsForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            desc = form.cleaned_data.get('desc')
            thumbnail = form.cleaned_data.get('thumbnail')
            content = form.cleaned_data.get('content')
            category_id = form.cleaned_data.get('category')
            pk = form.cleaned_data.get("pk")
            category = NewsCategory.objects.get(pk=category_id)
            News.objects.filter(pk=pk).update(title=title, desc=desc, thumbnail=thumbnail, content=content,
                                              category=category)
            return restful.ok()
        else:
            return restful.params_error(message=form.get_errors())


@require_POST
@permission_required(perm="news.delete_news", login_url='/')
def delete_news(request):
    news_id = request.POST.get('news_id')
    News.objects.filter(pk=news_id).delete()
    return restful.ok()

# 课程
