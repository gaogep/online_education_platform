__author__ = 'Zpf'
__date__ = '2019/7/5 下午6:01'

from django.conf.urls import url

from .views import UserInfoView, UploadImageView, ChangePwdView, MyMessageView, \
    SendCodeView, UpdateEmailView, MyCourseView, MyFavOrgView, MyFavTeacherView, MyFavCourseView


urlpatterns = [
    # 用户信息
    url('^info/$', UserInfoView.as_view(), name="user_info"),

    # 用户头像上传
    url('^image/upload/$', UploadImageView.as_view(), name="image_upload"),

    # 个人中心更新密码
    url('^update/pwd/$', ChangePwdView.as_view(), name="update_pwd"),

    # 往邮箱发送验证码
    url('^sendemail_code/$', SendCodeView.as_view(), name="send_code"),

    # 修改邮箱
    url('^update_email/$', UpdateEmailView.as_view(), name="update_email"),

    # 我的课程
    url('^my_course/$', MyCourseView.as_view(), name="my_course"),

    # 我收藏的课程机构
    url('^myfav/org/$', MyFavOrgView.as_view(), name="myfav_org"),

    # 我收藏的课程机构
    url('^myfav/teacher/$', MyFavTeacherView.as_view(), name="myfav_teacher"),

    # 我收藏的课程
    url('^myfav/course/$', MyFavCourseView.as_view(), name="myfav_course"),

    # 我的消息
    url('^my_message/$', MyMessageView.as_view(), name="my_message"),

]