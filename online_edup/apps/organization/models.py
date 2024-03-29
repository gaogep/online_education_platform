from datetime import datetime

from django.db import models


class CityDict(models.Model):
    name = models.CharField(max_length=20, verbose_name='城市名')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')
    desc = models.CharField(max_length=200, verbose_name='城市描述')

    class Meta:
        verbose_name = '城市'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseOrg(models.Model):
    name = models.CharField(max_length=50, verbose_name='机构名称')
    tag = models.CharField(max_length=10, verbose_name='标签', default='知名机构')
    desc = models.TextField(verbose_name='机构描述')
    category = models.CharField(max_length=20, choices=(('px', '培训机构'), ('gr', '个人'), ('gx', '高校')),
                                verbose_name='机构类别', default='px')
    click_nums = models.IntegerField(default=0, verbose_name="点击数")
    fav_nums = models.IntegerField(default=0, verbose_name="收藏数")
    image = models.ImageField(max_length=200, upload_to='org/%Y/%m', verbose_name='封面图')
    address = models.CharField(max_length=150, verbose_name='机构地址')
    city = models.ForeignKey(CityDict, verbose_name='所在城市')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')
    students = models.IntegerField(default=0, verbose_name="学习人数")
    courses = models.IntegerField(default=0, verbose_name="课程数")

    class Meta:
        verbose_name = '课程机构'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def get_teachers(self):
        return self.teacher_set.all().count()


class Teacher(models.Model):
    org = models.ForeignKey(CourseOrg, verbose_name='所属机构')
    name = models.CharField(max_length=50, verbose_name='教师名称')
    work_years = models.IntegerField(verbose_name='工作年限')
    work_company = models.CharField(max_length=50, verbose_name='就职公司')
    work_position = models.CharField(max_length=50, verbose_name='职位')
    points = models.CharField(max_length=50, verbose_name='教学特点')
    click_nums = models.IntegerField(default=0, verbose_name="点击数")
    fav_nums = models.IntegerField(default=0, verbose_name="收藏数")
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')
    image = models.ImageField(max_length=200, upload_to='teacher/%Y/%m', verbose_name='头像', default='')
    age = models.IntegerField(verbose_name='年龄', default=25)

    class Meta:
        verbose_name = '教师'
        verbose_name_plural = verbose_name

    def get_couse_numbers(self):
        return self.course_set.all().count()

    def __str__(self):
        return self.name
