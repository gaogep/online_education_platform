import json

from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.views.generic.base import View
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from django.core.urlresolvers import reverse
from pure_pagination import Paginator, PageNotAnInteger

from courses.models import Course
from operation.models import UserCourse, UserFavorite, UserMessage
from organization.models import CourseOrg, Teacher
from .models import UserProfile, EmailVerifyRecord, Banner
from .forms import LoginForm, RegisterForm, ForgetForm, ModifyPwdForm, UploadImageForm, UserInfoForm
from utils.send_email import send_email_sync
from utils.mixin_utils import LoginRequiredMixin


class CustomBackend(ModelBackend):
    """重载用户登录的验证方法"""
    def authenticate(self, username=None, password=None, **kwargs):
        try:                               # 利用Q取并集达到也可以用email验证用户身份的目的
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class RegisterView(View):
    """用户注册"""
    def get(self, request):
        register_form = RegisterForm()
        return render(request, "register.html", {"register_form": register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get("email", "")
            if UserProfile.objects.filter(email=user_name):
                return render(request, "register.html", {"register_form": register_form, "msg": "用户已经存在"})
            pass_word = request.POST.get("password", "")
            user = UserProfile()
            user.username = user_name
            user.set_password(pass_word)
            user.is_active = False
            user.save()

            # 写入欢迎消息
            user_message = UserMessage()
            user_message.user = user.id
            user_message.message = "欢迎注册"
            user_message.save()

            send_email_sync(user_name, "register")
            return render(request, "login.html")
        else:
            return render(request, "register.html", {"register_form": register_form})


class LoginView(View):
    """用户登录"""
    def get(self, request):
        return render(request, "login.html")

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    # 重定向至index页面 如果直接render index页面中没有数据
                    return HttpResponseRedirect(reverse("index"))
                else:
                    return render(request, "login.html", {"msg": "用户未激活"})
            else:
                return render(request, "login.html", {"msg": "用户名或密码错误"})
        else:
            return render(request, "login.html", {"login_form": login_form})


class LogoutView(LoginRequiredMixin, View):
    """用户登出"""
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse("index"))


class ActiveUserView(View):
    """激活用户"""
    def get(self, request, active_code):
        records = EmailVerifyRecord.objects.filter(code=active_code)
        if records:
            for record in records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
        else:
            return render(request, 'active_failed.html')
        return render(request, "login.html")


class ForgetView(View):
    """找回密码"""
    def get(self, request):
        forget_form = ForgetForm()
        return render(request, 'forgetpwd.html', {"forget_form": forget_form})

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get("email", "")
            send_email_sync(email, "forget")
            return render(request, 'send_success.html')
        else:
            return render(request, 'forgetpwd.html', {"forget_form": forget_form})


class ResetView(View):
    """获取重置密码页面"""
    def get(self, request, active_code):
        records = EmailVerifyRecord.objects.filter(code=active_code)
        if records:
            for record in records:
                email = record.email
                return render(request, 'password_reset.html', {"email": email})  # 把email放到hiddent_input中
        else:
            return render(request, 'active_failed.html')
        return render(request, 'login.html')


class ModifyPwdView(View):
    """修改密码"""
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        email = request.POST.get("email", "")
        if modify_form.is_valid():
            pwd = request.POST.get("password", "")
            pwd2 = request.POST.get("password2", "")
            if pwd != pwd2:
                return render(request, 'password_reset.html', {"email": email, "msg": "密码不一致"})
            user = UserProfile.objects.get(email=email)
            user.set_password(pwd)
            user.save()
            return render(request, 'login.html')
        else:
            return render(request, 'password_reset.html', {"email": email, "modify_form": modify_form})


class UserInfoView(LoginRequiredMixin, View):
    """用户个人信息"""
    def get(self, request):
        return render(request, 'usercenter-info.html', {})

    # 注意,这里是修改,不是新增,所以要添加一个instance
    def post(self, request):
        user_info_form = UserInfoForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(user_info_form.errors), content_type='application/json')


class UploadImageView(LoginRequiredMixin, View):
    """用户修改头像"""
    def post(self, request):
        # 利用ModelForm修改头像
        form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return HttpResponse("{'status': 'success'}", content_type='application/json')
        else:
            return HttpResponse("{'status': 'fail'}", content_type='application/json')


class ChangePwdView(View):
    """修改密码"""
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd = request.POST.get("password", "")
            pwd2 = request.POST.get("password2", "")
            if pwd != pwd2:
                return HttpResponse("{'status': 'fail'}", content_type='application/json')
            user = request.user
            user.set_password(pwd)
            user.save()
            return HttpResponse("{'status': 'success'}", content_type='application/json')
        else:
            return HttpResponse(json.dumps(modify_form.errors), content_type='application/json')


class SendCodeView(LoginRequiredMixin, View):
    """发送邮箱验证码"""
    def get(self, request):
        email = request.GET.get("email", "")
        if UserProfile.filter(email=email):
            return HttpResponse("{'email': '邮箱已经存在'}", content_type='application/json')
        send_email_sync(email, "update")
        return HttpResponse("{'status': 'success'}", content_type='application/json')


class UpdateEmailView(LoginRequiredMixin, View):
    """修改个人邮箱"""
    def post(self, request):
        email = request.POST.get("email", "")
        code = request.POST.get("code", "")
        existed_record = EmailVerifyRecord.objects.filter(email=email, code=code, send_type="update")
        if existed_record:
            user = request.user
            user.email = email
            user.save()
            return HttpResponse("{'status': 'success'}", content_type='application/json')
        else:
            return HttpResponse("{'email': '验证码出错'}", content_type='application/json')


class MyCourseView(LoginRequiredMixin, View):
    """我的课程"""
    def get(self, request):
        user_courses = UserCourse.objects.filter(user=request.user)
        return render(request, 'usercenter-mycourse.html', {
            'user_courses': user_courses
        })


class MyFavOrgView(LoginRequiredMixin, View):
    """我收藏的课程机构"""
    def get(self, request):
        org_list = []
        fav_orgs = UserFavorite.objects.filter(user=request.user, fav_type=2)
        for fav_org in fav_orgs:
            org_id = fav_org.id
            org_list.append(CourseOrg.objects.get(id=org_id))
        return render(request, 'usercenter-fav-org.html', {
            'org_list': org_list
        })


class MyFavTeacherView(LoginRequiredMixin, View):
    """我收藏的授课教师"""
    def get(self, request):
        t_list = []
        fav_teachers = UserFavorite.objects.filter(user=request.user, fav_type=3)
        for fav_teacher in fav_teachers:
            t_id = fav_teacher.id
            t_list.append(Teacher.objects.get(id=t_id))
        return render(request, 'usercenter-fav-teacher.html', {
            't_list': t_list
        })


class MyFavCourseView(LoginRequiredMixin, View):
    """我收藏的课程"""
    def get(self, request):
        c_list = []
        fav_courses = UserFavorite.objects.filter(user=request.user, fav_type=1)
        for fav_course in fav_courses:
            c_id = fav_course.id
            c_list.append(Course.objects.get(id=c_id))
        return render(request, 'usercenter-fav-course.html', {
            'c_list': c_list
        })


class MyMessageView(LoginRequiredMixin, View):
    """我的消息"""
    def get(self, request):
        all_messages = UserMessage.objects.filter(user=request.user.id)
        all_unread_messages = UserMessage.objects.filter(user=request.user.id, has_read=False)

        # 过滤消息
        for unread_message in all_unread_messages:
            unread_message.has_read = True
            unread_message.save()

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_messages, request=request, per_page=5)
        messages = p.page(page)
        return render(request, 'usercenter-message.html', {
            'messages': messages
        })


class IndexView(View):
    def get(self, request):
        all_banners = Banner.objects.all().order_by('index')
        courses = Course.objects.filter(is_banner=False)[:6]
        bnner_courses = Course.objects.filter(is_banner=True)[:3]
        course_orgs = CourseOrg.objects.all()[:15]
        return render(request, 'index.html', {
            'all_banners': all_banners,
            'courses': courses,
            'bnner_courses': bnner_courses,
            'course_orgs': course_orgs
        })


def page_not_found(request):
    # 全局404处理函数
    from django.shortcuts import render_to_response
    response = render_to_response('404.html', {})
    response.status_code = 404
    return response


def page_error(request):
    # 全局404处理函数
    from django.shortcuts import render_to_response
    response = render_to_response('500.html', {})
    response.status_code = 500
    return response
