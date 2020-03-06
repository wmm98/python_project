from ..forms import FormMixin
from django import forms
from ..news.models import News, Banner
from ..course.models import Course
from ..payinfo.models import Payinfo


class PayInfoForm(forms.ModelForm, FormMixin):
    class Meta:
        model = Payinfo
        fields = ('title', 'profile', 'path', 'price')


class EditNewsCategoryForm(forms.Form):
    pk = forms.IntegerField(error_messages={"required": "必须传入分类的id"})
    name = forms.CharField(max_length=100)


class WriteNewsForm(forms.ModelForm, FormMixin):
    category = forms.IntegerField()

    class Meta:
        model = News
        exclude = ['category', 'author', 'pub_time']


class AddBannerForm(forms.ModelForm, FormMixin):
    class Meta:
        model = Banner
        fields = ('priority', 'link_to', 'image_url')


class EditBannerForm(forms.ModelForm, FormMixin):
    pk = forms.IntegerField()

    class Meta:
        model = Banner
        fields = ('priority', 'link_to', 'image_url')


class EditNewsForm(forms.ModelForm, FormMixin):
    category = forms.IntegerField()
    pk = forms.IntegerField()

    class Meta:
        model = News
        exclude = ['category', 'author', 'pub_time']


class PubCourseForm(forms.ModelForm, FormMixin):
    category_id = forms.IntegerField()
    teacher_id = forms.IntegerField()

    class Meta:
        model = Course
        exclude = ["category", 'teacher']


class EditCourseCategoryForm(forms.Form):
    pk = forms.IntegerField(error_messages={"required": "必须传入分类的id"})
    name = forms.CharField(max_length=100)


class EeditCourseForm(forms.ModelForm, FormMixin):
    category_id = forms.IntegerField()
    teacher_id = forms.IntegerField()
    pk = forms.IntegerField()

    class Meta:
        model = Course
        exclude = ["category", 'teacher', 'pub_time']
