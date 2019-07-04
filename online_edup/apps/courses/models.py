from datetime import datetime

from django.db import models

from organization.models import CourseOrg, Teacher


class Course(models.Model):
    course_org = models.ForeignKey(CourseOrg, verbose_name='授课机构', null=True, blank=True)
    name = models.CharField(max_length=100, verbose_name='课程名')
    desc = models.CharField(max_length=300, verbose_name='课程描述')
    detail = models.TextField(verbose_name='课程详情')
    degree = models.CharField(max_length=2, choices=(('cj', '初级'), ('zj', '中级'), ('gj', '高级')), verbose_name='难度')
    times = models.IntegerField(default=0, verbose_name='学习时长(分钟数)')
    students = models.IntegerField(verbose_name='学习人数')
    fav_nums = models.IntegerField(verbose_name='收藏人数')
    click_nums = models.IntegerField(default=0, verbose_name='点击数')
    image = models.ImageField(max_length=200, upload_to='courses/%Y/%m', verbose_name='封面图')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')
    category = models.CharField(max_length=20, verbose_name='课程类别', default='后端开发')
    tag = models.CharField(max_length=10, verbose_name='标签', default='')
    teacher = models.ForeignKey(Teacher, verbose_name='讲师', null=True, blank=True)

    class Meta:
        verbose_name = '课程'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def get_chapter_nums(self):
        # 获取课程章节数
        return self.lesson_set.all().count()

    def get_students(self):
        # 获取学习这门课程的人的头像
        return self.usercourse_set.all()[:5]

    def get_course_lesson(self):
        # 获取课程所有章节
        return self.lesson_set.all()


class Lesson(models.Model):
    course = models.ForeignKey(Course, verbose_name='课程')
    name = models.CharField(max_length=100, verbose_name='章节名')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '章节'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.course.name}->{self.name}'

    def get_lesson_video(self):
        # 获取章节视频
        return self.video_set.all()


class Video(models.Model):
    lesson = models.ForeignKey(Lesson, verbose_name='章节名')
    name = models.CharField(max_length=100, verbose_name='视频名')
    url = models.CharField(max_length=200, verbose_name='视频地址', default='')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')
    times = models.IntegerField(default=0, verbose_name='学习时长(分钟数)')

    class Meta:
        verbose_name = '视频'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.lesson.name}->{self.name}'


class CourseResource(models.Model):
    course = models.ForeignKey(Course, verbose_name='课程')
    name = models.CharField(max_length=100, verbose_name='资源名')
    download = models.FileField(max_length=100, upload_to='course/resource/%Y/%m', verbose_name='资源文件')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '课程资源'
        verbose_name_plural = verbose_name
