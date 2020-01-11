from django.shortcuts import render


def index(request):
    return render(request, 'news/index.html')


# 新闻详情页面
def news_detail(request, news_id):
    return render(request, 'news/news_detail.html')


# 搜索页面
def search(request):
    return render(request, 'search/search.html')