from django.shortcuts import render
from .serializers import NewsSerializer, CommentSerizlizer
from .models import News, NewsCategory, Comment, Banner
from django.conf import settings
from ..utils import restful
from django.http import JsonResponse, HttpResponse
from django.http import Http404
from .forms import PublicCommentForm
from ..xfzauth.decorators import xfz_login_required
from django.db.models import Q


def index(request):
    # 默认展开2篇新闻
    count = settings.ONE_PAGE_NEWS_COUNT
    newses = News.objects.select_related('category', 'author').all()[0:count]
    categories = NewsCategory.objects.all()
    context = {
        'newses': newses,
        'categories': categories,
        'banners': Banner.objects.all(),
    }
    return render(request, 'news/index.html', context=context)


def news_list(request):
    # 通过p参数，来指定要获取第几页的数据
    # 并且这个p参数，是通过查询字符串的方式传过来的/news/list/?p=2
    page = int(request.GET.get('p', 1))
    # 分类为0：代表不进行任何分类，直接按照时间倒序排序
    category_id = int(request.GET.get('category_id', 0))
    # 0,1
    # 2,3
    # 4,5
    start = (page - 1) * settings.ONE_PAGE_NEWS_COUNT
    end = start + settings.ONE_PAGE_NEWS_COUNT

    if category_id == 0:
        # QuerySet
        # {'id':1,'title':'abc',category:{"id":1,'name':'热点'}}
        newses = News.objects.select_related('category', 'author').all()[start:end]
    else:
        newses = News.objects.select_related('category', 'author').filter(category__id=category_id)[start:end]
    serializer = NewsSerializer(newses, many=True)
    data = serializer.data
    return restful.result(data=data)


# 新闻详情页面
def news_detail(request, news_id):
    try:
        news = News.objects.select_related('category', 'author').prefetch_related("comments__author").get(pk=news_id)
        # news = News.objects.get(pk=news_id)
        context = {
            'news': news
        }
        return render(request, 'news/news_detail.html', context=context)
    except News.DoesNotExist:
        return HttpResponse("您找的页面不存在")


@xfz_login_required
def public_comment(request):
    form = PublicCommentForm(request.POST)
    if form.is_valid():
        news_id = form.cleaned_data.get('news_id')
        content = form.cleaned_data.get('content')
        news = News.objects.get(pk=news_id)
        comment = Comment.objects.create(content=content, news=news, author=request.user)
        serizlize = CommentSerizlizer(comment)
        return restful.result(data=serizlize.data)
    else:
        return restful.params_error(message=form.get_errors())


# 搜索页面
def search(request):
    q = request.GET.get('q')
    context = {}
    if q:
        newses = News.objects.filter(Q(title__icontains=q) | Q(content__icontains=q))
        num = News.objects.filter(Q(title__icontains=q) | Q(content__icontains=q)).count()
        print("==========================================")
        print(num)
        print(newses)
        print("==========================================")
        context['newses'] = newses
        context['num'] = num

    return render(request, 'search/search.html', context=context)
