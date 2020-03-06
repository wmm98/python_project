# encoding: utf-8
from django.shortcuts import render
from .forms import PubCourseForm, EditCourseCategoryForm, EeditCourseForm
from ..course.models import Course, CourseCategory, Teacher
from django.views.generic import View
from ..utils import restful
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required
from django.views.decorators.http import require_POST, require_GET
from datetime import datetime
from django.utils.timezone import make_aware
from django.core.paginator import Paginator
from urllib import parse
from django.db.models import Sum, Count


#
@method_decorator(permission_required(perm="course.add_course", login_url='/'), name='dispatch')
class PubCourse(View):
    def get(self, request):
        context = {
            'categories': CourseCategory.objects.all(),
            'teachers': Teacher.objects.all()
        }
        return render(request, 'cms/pub_course.html', context=context)

    def post(self, request):
        form = PubCourseForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            category_id = form.cleaned_data.get('category_id')
            video_url = form.cleaned_data.get('video_url')
            cover_url = form.cleaned_data.get("cover_url")
            price = form.cleaned_data.get('price')
            duration = form.cleaned_data.get('duration')
            profile = form.cleaned_data.get('profile')
            teacher_id = form.cleaned_data.get('teacher_id')

            category = CourseCategory.objects.get(pk=category_id)
            teacher = Teacher.objects.get(pk=teacher_id)

            Course.objects.create(title=title, video_url=video_url, cover_url=cover_url, price=price, duration=duration,
                                  profile=profile, category=category, teacher=teacher)
            return restful.ok()
        else:
            return restful.params_error(message=form.get_errors())


# 课程分类
@require_GET
@permission_required(perm="course.add_coursecategory", login_url='/')
def course_category(request):
    categories = CourseCategory.objects.all()
    # 计算课程相关总类的数量
    # 默认根据id排序
    # category_sum = CourseCategory.objects.annotate(category_num=Count("course__category")).values('category_num')
    # print(len(Course.objects.all()))
    # print("==================")
    # total_category = []
    # categories_num = []
    # for category in categories:
    #     categories_num.append(category)
    # print(categories_num)

    # for category in categories:
    #     total_category.append()

    # for i in category_sum:
    #     # print(i.category_num)
    #     print(i)
    #     print(type(i))
        # categories_num.append(i.category_num)

    # for j in categories:
    #     print(i.values)

    context = {
        'categories': categories,
    }
    return render(request, 'cms/course_category.html', context=context)


# 添加 课程分类
@require_POST
@permission_required(perm="course.add_coursecategory", login_url='/')
def add_course_category(request):
    name = request.POST.get("name")
    # 判断分类是否存在
    exists = CourseCategory.objects.filter(name=name).exists()
    if not exists:
        # 添加
        CourseCategory.objects.create(name=name)
        return restful.ok()
    else:
        return restful.params_error(message="该分类已经存在！")


# 编辑 课程分类
@require_POST
@permission_required(perm="course.change_coursecategory", login_url='/')
def edit_course_category(request):
    form = EditCourseCategoryForm(request.POST)
    if form.is_valid():
        pk = form.cleaned_data.get("pk")
        name = form.cleaned_data.get("name")
        try:
            CourseCategory.objects.filter(pk=pk).update(name=name)
            return restful.ok()
        except:
            return restful.params_error(message="该分类不存在")
    else:
        return restful.params_error(message=form.get_errors())


# 删除分类
@require_POST
@permission_required(perm="course.delete_coursecategory", login_url='/')
def delete_course_category(request):
    pk = request.POST.get("pk")
    print(pk)
    try:
        CourseCategory.objects.filter(pk=pk).delete()
        return restful.ok()
    except:
        return restful.unauth(message='该分类不存在！')


# 课程列表
@method_decorator(permission_required(perm="course.change_course", login_url='/'), name='dispatch')
class CourseListView(View):
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

        courses = Course.objects.select_related('category', 'teacher')

        if start or end:
            if start:
                start_date = datetime.strptime(start, '%Y/%m/%d')
            else:
                start_date = datetime(year=2018, month=6, day=1)
            if end:
                end_date = datetime.strptime(end, '%Y/%m/%d')
            else:
                end_date = datetime.today()
            courses = courses.filter(pub_time__range=(make_aware(start_date), make_aware(end_date)))

        if title:
            courses = courses.filter(title__icontains=title)

        if category_id:
            courses = courses.filter(category=category_id)

        paginator = Paginator(courses, 4)
        page_obj = paginator.page(page)

        context_data = self.get_pagination_data(paginator, page_obj)

        context = {
            'categories': CourseCategory.objects.all(),
            'courses': page_obj.object_list,
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
        return render(request, 'cms/course_list.html', context=context)

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


@method_decorator(permission_required(perm="course.change_course", login_url='/'), name='dispatch')
class EditCourseView(View):
    def get(self, request):
        print("-------------------------")
        course_id = request.GET.get('course_id')
        course = Course.objects.get(pk=course_id)
        context = {
            'course': course,
            'categories': CourseCategory.objects.all(),
            'teachers': Teacher.objects.all()
        }
        return render(request, 'cms/pub_course.html', context=context)

    def post(self, request):
        print("==============================")
        form = EeditCourseForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            category_id = form.cleaned_data.get('category_id')
            video_url = form.cleaned_data.get('video_url')
            cover_url = form.cleaned_data.get("cover_url")
            price = form.cleaned_data.get('price')
            duration = form.cleaned_data.get('duration')
            profile = form.cleaned_data.get('profile')
            teacher_id = form.cleaned_data.get('teacher_id')
            pk = form.cleaned_data.get("pk")
            Course.objects.filter(pk=pk).update(title=title, profile=profile, duration=duration, price=price,
                                                teacher_id=teacher_id, cover_url=cover_url, video_url=video_url, category_id=category_id)
            return restful.ok()
        else:
            return restful.params_error(message=form.get_errors())


@require_POST
@permission_required(perm="course.delete_course", login_url='/')
def delete_course(request):
    course_id = request.POST.get('course_id')
    Course.objects.filter(pk=course_id).delete()
    return restful.ok()


