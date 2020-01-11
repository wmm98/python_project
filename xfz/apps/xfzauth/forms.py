from django import forms
from apps.forms import FormMixin


class LoginForm(forms.Form, FormMixin):
    telephone = forms.CharField(max_length=11)
    password = forms.CharField(max_length=20, min_length=6, error_messages={"max_length": "密码最多不能超过20哥字符",
                                                                            "min_length": "密码不能少于6个字符"})
    remember = forms.IntegerField(required=False)
