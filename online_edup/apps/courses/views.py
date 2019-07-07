from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
from django.db.models import Q

from pure_pagination import Paginator, PageNotAnInteger

from .models import Course, CourseResource, Video
from operation.models import UserFavorite, CourseComment, UserCourse
from utils.mixin_utils import LoginRequiredMixin


class CourseListView(View):
    """课程列表"""
    def get(self, request):
        all_courses = Course.objects.all().order_by("-add_time")

        hot_courses = all_courses.order_by("-click_nums")[:3]

        # 搜索功能 根据关键词对课程名进行过滤 类似SQL中的Like
        search_keywords = request.GET.get("keywords", "")
        if search_keywords:
            all_courses = all_courses.filter(Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords) |
                                             Q(detail__icontains=search_keywords))

        # 课程排序
        sort = request.GET.get('sort', '')
        if sort:
            if sort == "students":
                all_courses = all_courses.order_by("-students")
            elif sort == "hot":
                all_courses = all_courses.order_by("-click_nums")

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_courses, request=request, per_page=3)
        courses = p.page(page)

        return render(request, 'course-list.html', {
            'all_courses': courses,
            'sort': sort,
            'hot_courses': hot_courses
        })


class CourseDetailView(View):
    """课程详情"""
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        course.click_nums += 1
        course.save()

        has_fav_course = False
        has_fav_org = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                has_fav_course = True
            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                has_fav_org = True

        # 利用tag进行相关课程推荐
        tag = course.tag
        related_course = []
        if tag:
            related_course = Course.objects.filter(tag=tag)[:1]
        return render(request, 'course-detail.html', {
            'course': course,
            'related_course': related_course,
            'has_fav_course': has_fav_course,
            'has_fav_org': has_fav_org
        })


class CourseInfoView(LoginRequiredMixin, View):
    """课程章节信息"""
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        course.students += 1
        course.save()
        all_resources = CourseResource.objects.filter(course=course)
        # 查询用户是否关联了该课程
        user_course = UserCourse.objects.filter(user=request.user, course=course)
        if not user_course:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()

        # 获取学过这门课程其他用户学过的课程
        related_courses = []
        user_courses = UserCourse.objects.filter(course=course)
        if user_courses:
            user_ids = [user_course.id for user_course in user_courses]
            all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
            course_ids = [user_course.course.id for user_course in all_user_courses]
            related_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:5]

        return render(request, 'course-video.html', {
            'course': course,
            'all_resources': all_resources,
            'related_courses': related_courses
        })


class CommentView(View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        all_comments = CourseComment.objects.filter(course=course)
        return render(request, 'course-comment.html', {
            'course': course,
            'all_comments': all_comments
        })


class AddComment(View):
    """添加课程评论"""
    def post(self, request):
        # 判断用户是否登录 没登录不能评论
        if not request.user.is_authenticated():
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')
        course_id = request.POST.get('course_id', 0)
        comments = request.POST.get('comments', 0)
        if int(course_id) > 0 and comments:
            course_comment = CourseComment()
            course_comment.course = Course.objects.get(id=int(course_id))
            course_comment.user = request.user
            course_comment.comments = comments
            course_comment.save()
            return HttpResponse('{"status":"success", "msg":"评论成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"评论失败"}', content_type='application/json')


class VideoPlay(View):
    """视频播放页面"""
    def get(self, request, video_id):
        video = Video.objects.get(id=int(video_id))
        course = video.lesson.course
        all_resources = CourseResource.objects.filter(course=course)

        # 查询用户是否关联了该课程
        user_course = UserCourse.objects.filter(user=request.user, course=course)
        if not user_course:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()

        # 获取学过这门课程其他用户学过的课程
        related_courses = []
        user_courses = UserCourse.objects.filter(course=course)
        if user_courses:
            user_ids = [user_course.id for user_course in user_courses]
            all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
            course_ids = [user_course.course.id for user_course in all_user_courses]
            related_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:5]

        return render(request, 'course-play.html', {
            'course': course,
            'all_resources': all_resources,
            'related_courses': related_courses,
            'video': video
        })
