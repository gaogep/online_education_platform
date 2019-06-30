__author__ = 'Zpf'
__date__ = '2019/6/29 下午6:26'

from django.conf.urls import url

from .views import OrgView, AddUserAskView, OrgHomeView, \
    OrgCourseView, OrgDescView, OrgTeacherView, AddFavView


urlpatterns = [
    # 授课机构相关url
    url('^list/$', OrgView.as_view(), name="org_list"),

    # 配置上传文件的访问处理函数
    url('^add_ask/$', AddUserAskView.as_view(), name="add_ask"),
    url('^home/(?P<org_id>\d+)/$', OrgHomeView.as_view(), name="org_home"),
    url('^course/(?P<org_id>\d+)/$', OrgCourseView.as_view(), name="org_course"),
    url('^desc/(?P<org_id>\d+)/$', OrgDescView.as_view(), name="org_desc"),
    url('^teacher/(?P<org_id>\d+)/$', OrgTeacherView.as_view(), name="org_teacher"),

    # 机构收藏
    url('^add_fav/$', AddFavView.as_view(), name="add_fav"),
]
