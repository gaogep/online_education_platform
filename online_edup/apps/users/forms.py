__author__ = 'Zpf'
__date__ = '2019/6/24 下午8:42'

from django import forms
from captcha.fields import CaptchaField


class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True)
    captcha = CaptchaField(required=True, error_messages={"invalid": "验证码错误"})


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=5)


class ForgetForm(forms.Form):
    email = forms.EmailField(required=True)
    captcha = CaptchaField(required=True, error_messages={"invalid": "验证码错误"})


class ModifyPwdForm(forms.Form):
    password = forms.CharField(required=True, min_length=5)
    password2 = forms.CharField(required=True, min_length=5)
