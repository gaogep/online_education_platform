__author__ = 'Zpf'
__date__ = '2019/6/25 下午9:32'

from random import Random
from threading import Thread

from django.core.mail import send_mail

from users.models import EmailVerifyRecord
from utils import main_url
from online_edup.settings import EMAIL_FROM


class EmailSendTypeError(Exception):
    pass


def generate_random_str(randomlength=8):
    strs = ''
    chars = 'AaBbCcDdEeFfJjHhIiGgkKlLmMNnOoPpQqRsWxyYz0983712456'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        strs += chars[random.randint(0, length)]
    return strs


def send_email(email, send_type="register"):
    email_record = EmailVerifyRecord()
    code = generate_random_str(4)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()
    if send_type == "register":
        email_title = "注册"
        email_body = "请点击下面的链接激活你的账号 http://" + main_url + "/active/" + f"{code}"
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass
    elif send_type == "forget":
        email_title = "找回密码"
        email_body = "请点击下面的链接找回你的密码 http://" + main_url + "/reset/" + f"{code}"
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass
    elif send_type == "update":
        email_title = "修改邮箱"
        email_body = f"你的验证码为: {code}"
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass
    else:
        raise EmailSendTypeError('邮件发送类型错误')


def send_email_sync(email, send_type="register"):
    email_thread = Thread(target=send_email, args=(email, send_type,))
    email_thread.start()
