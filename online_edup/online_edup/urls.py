"""online_edup URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.views.static import serve

import xadmin

from online_edup.settings import MEDIA_ROOT, STATIC_ROOT
from users.views import IndexView, LoginView, LogoutView, RegisterView, ActiveUserView, ForgetView, ResetView, ModifyPwdView


urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url('^$', IndexView.as_view(), name="index"),
    url('^login/$', LoginView.as_view(), name="login"),
    url('^logout/$', LogoutView.as_view(), name="logout"),
    url('^register/$', RegisterView.as_view(), name="register"),
    url('^captcha/', include('captcha.urls')),
    url('^active/(?P<active_code>.*)/$', ActiveUserView.as_view(), name="user_active"),
    url('^forget/$', ForgetView.as_view(), name="forgetpwd"),
    url('^reset/(?P<active_code>.*)/$', ResetView.as_view(), name="resetpwd"),
    url('^modifypwd/$', ModifyPwdView.as_view(), name="modifypwd"),

    # 配置上传文件的处理函数
    url('^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),

    # 配置上传文件的处理函数
    url('^static/(?P<path>.*)$', serve, {'document_root': STATIC_ROOT}),

    # 课程机构url配置
    url('^org/', include('organization.urls', namespace="org")),

    # 课程相关url配置
    url('^course/', include('courses.urls', namespace="course")),

    # 用户相关url配置
    url('^users/', include('users.urls', namespace="users")),
]
