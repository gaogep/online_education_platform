from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.views.generic.base import View
from django.db.models import Q

from .models import UserProfile, EmailVerifyRecord
from .forms import LoginForm, RegisterForm, ForgetForm, ModifyPwdForm
from utils.send_email import send_email_sync


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
                    return render(request, "index.html", {})
                else:
                    return render(request, "login.html", {"msg": "用户未激活"})
            else:
                return render(request, "login.html", {"msg": "用户名或密码错误"})
        else:
            return render(request, "login.html", {"login_form": login_form})


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
    """重置密码"""
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



