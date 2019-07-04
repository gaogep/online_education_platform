__author__ = 'Zpf'
__date__ = '2019/6/22 下午7:38'

import xadmin

from .models import Course, CourseResource, Lesson, Video


class CourseAdmin:
    list_display = ['course_org', 'name', 'desc', 'detail', 'degree', 'times', 'tag', 'teacher',
                    'category', 'students', 'fav_nums', 'click_nums', 'image', 'add_time']
    search_fields = ['course_org', 'name', 'desc', 'detail', 'degree', 'times', 'tag', 'teacher',
                     'category', 'students', 'fav_nums', 'click_nums', 'image']
    list_filter = ['course_org', 'name', 'desc', 'detail', 'degree', 'times', 'tag', 'teacher',
                   'category', 'students', 'fav_nums', 'click_nums', 'image', 'add_time']


class LessonAdmin:
    list_display = ['course', 'name', 'add_time']
    search_fields = ['course', 'name']
    list_filter = ['course__name', 'name', 'add_time']  # 搜索中以" __ "添加外键的名称


class ViedoAdmin:
    list_display = ['lesson', 'name', 'add_time']
    search_fields = ['lesson', 'name']
    list_filter = ['lesson__name', 'name', 'add_time']


class CourseResourceAdmin:
    list_display = ['course', 'name', 'download', 'add_time']
    search_fields = ['course', 'name', 'download']
    list_filter = ['course__name', 'name', 'download', 'add_time']


xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, ViedoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
