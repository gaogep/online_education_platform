__author__ = 'Zpf'
__date__ = '2019/7/2 下午5:22'

from django.conf.urls import url

from .views import CourseListView, CourseDetailView, CourseInfoView, CommentView, AddComment, VideoPlay


urlpatterns = [
    # 课程列表页
    url('^list/$', CourseListView.as_view(), name='course_list'),

    # 课程详情页
    url('^detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name='course_detail'),

    # 课程章节信息
    url('^chapterinfo/(?P<course_id>\d+)/$', CourseInfoView.as_view(), name='course_chapterinfo'),

    # 课程评论
    url('^comment/(?P<course_id>\d+)/$', CommentView.as_view(), name='course_comment'),

    # 添加课程评论
    url('^comment/$', AddComment.as_view(), name='add_comment'),

    url('^video/(?P<video_id>\d+)/$', VideoPlay.as_view(), name='video_play'),

]


