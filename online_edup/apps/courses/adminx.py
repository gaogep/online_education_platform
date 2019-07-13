__author__ = 'Zpf'
__date__ = '2019/6/22 下午7:38'

import xadmin

from .models import Course, CourseResource, Lesson, Video, BannerCourse
from organization.models import CourseOrg


class LessonInline:
    model = Lesson
    extra = 0


class CourseResourceInline:
    model = CourseResource
    extra = 0


class CourseAdmin:                                                                              # 展示字段中添加函数可以直接调用
    list_display = ['course_org', 'name', 'desc', 'detail', 'degree', 'times', 'tag', 'teacher', 'get_chapter_nums', 'go_to',
                    'category', 'students', 'fav_nums', 'click_nums', 'image', 'add_time']
    search_fields = ['course_org', 'name', 'desc', 'detail', 'degree', 'times', 'tag', 'teacher',
                     'category', 'students', 'fav_nums', 'click_nums', 'image']
    list_filter = ['course_org', 'name', 'desc', 'detail', 'degree', 'times', 'tag', 'teacher',
                   'category', 'students', 'fav_nums', 'click_nums', 'image', 'add_time']
    ordering = ['-click_nums']  # 默认以点击数倒序排列
    readonly_fields = []        # 设置只读字段
    # exclude = []                不显示某些字段 和ordering冲突
    inlines = [LessonInline, CourseResourceInline]    # 章节管理器
    list_editable = ['degree', 'desc']    # 这里的字段在展示页面可以直接进行编辑
    refresh_times = [3, 5]      # 设置页面刷新间隔时间
    model_icon                  # 设置默认的icon

    def queryset(self):  # 通过字段过滤将课程分为课程和轮播课程两种不同的管理器
        qs = super().queryset()
        qs = qs.filter(is_banner=False)
        return qs

    def save_modesl(self):
        # 在保存（修改或者新增)课程的时候统计课程机构的课程数
        # new_obj是一个course对象
        obj = self.new_obj
        obj.save()
        course_org = obj.course_org
        if not course_org:
            return
        course_org.courses = Course.objects.filter(course_org=course_org).count()
        course_org.save()


class BannerCourseAdmin:
    list_display = ['course_org', 'name', 'desc', 'detail', 'degree', 'times', 'tag', 'teacher',
                    'category', 'students', 'fav_nums', 'click_nums', 'image', 'add_time']
    search_fields = ['course_org', 'name', 'desc', 'detail', 'degree', 'times', 'tag', 'teacher',
                     'category', 'students', 'fav_nums', 'click_nums', 'image']
    list_filter = ['course_org', 'name', 'desc', 'detail', 'degree', 'times', 'tag', 'teacher',
                   'category', 'students', 'fav_nums', 'click_nums', 'image', 'add_time']
    ordering = ['-click_nums']  # 默认以点击数倒序排列

    def queryset(self):
        qs = super().queryset()
        qs = qs.filter(is_banner=True)
        return qs


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
xadmin.site.register(BannerCourse, BannerCourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, ViedoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
