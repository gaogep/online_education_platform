__author__ = 'Zpf'
__date__ = '2019/7/3 下午9:38'

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# from django.contrib.auth.mixins import LoginRequiredMixin


class LoginRequiredMixin:
    # 将一个函数装饰器转化为一个方法装饰器
    @method_decorator(login_required(login_url='/login/'))
    def dispatch(self, request, *args, **kwargs):
        # 处理请求之前先用login_required进行登录判断 判断成功以后调用父类的dispatch的方法
        # 即调用View的dispatch方法
        return super().dispatch(request, *args, **kwargs)
