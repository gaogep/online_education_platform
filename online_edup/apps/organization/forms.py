__author__ = 'Zpf'
__date__ = '2019/6/29 下午6:03'

import re

from django import forms

from operation.models import UserAsk

# 一般form
# class UserAskForm(forms.Form):
#     name = forms.CharField(required=True, max_length=20, min_length=2)
#     phone = forms.CharField(required=True, min_length=11, max_length=11)
#     course_name = forms.CharField(required=True, max_length=50, min_length=5)


# 利用modelForm基于数据库模型生成表单
# 此类表单在验证通过以后可以直接保存到数据库中
class UserAskModelForm(forms.ModelForm):
    # my_fileds = forms.CharField()->也可以自定义表单域
    class Meta:
        model = UserAsk
        # 选取生成的表单需要的字段
        fields = ['name', 'mobile', 'course_name']

    # 表单内域内字段过滤函数,必须以clean开头,验证的时候自动调用
    def clean_mobile(self):
        """验证手机号码是否合法"""
        # 在待验证字典cleaned_data中取提交上来的数据
        mobile = self.cleaned_data['mobile']
        regex_mobile = ""
        if re.match(regex_mobile, mobile):
            return mobile
        else:
            raise forms.ValidationError('手机号码非法', code='mobile_invalid')
