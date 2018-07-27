import jwt
import json
import redis
import datetime
from celery.decorators import task
from django.http import JsonResponse
from django.db.models import Func, Value
from django.core.mail import EmailMessage
from .apps import email_check_template, email_forget_template
from .models import User

send_email_pool = redis.StrictRedis(host='127.0.0.1', port=6379, db=1)
FRONTEND_URL = 'http://www.chao6hui.cn/views/index.html'
BACKEND_URL = 'https://lab.zxh326.cn/api/'

@task(bind=True, max_retries=3, default_retry_delay=10)
def send_check_email(self, uid, username, email, fail_silently=False):
    subject = '【SSZ国际魔方联赛】邮箱验证'
    to_list = [email]
    token = BACKEND_URL + "auth/checkemail?token="+ gen_jwt(uid, username, 'checkemail')
    html_content = email_check_template.format(username=username, token=token)
    try:
        msg = EmailMessage(subject, html_content, None, to_list)
        msg.content_subtype = "html"
        msg.send(fail_silently)
        send_email_pool.set('sendemail:{}'.format(email), 1, ex=180)
    except Exception as e:
        raise self.retry(exc=e)

    return email


@task(bind=True, max_retries=3, default_retry_delay=10)
def forget_password_email(self, email, fail_silently=False):
    subject = '【SSZ国际魔方联赛】重置密码'
    uid = User.get_user_by_email(email)
    if not uid:
        return 
    uid = uid.id
    to_list = [email]
    token = FRONTEND_URL +"?token=" + gen_jwt(uid, email, 'resetpassword', 0.17)
    html_content = email_forget_template.format(email=email, token=token)
    try:
        if not send_email_pool.exists('sendemail:{}'.format(email)):
            msg = EmailMessage(subject, html_content, None, to_list)
            msg.content_subtype = "html"
            msg.send(fail_silently)
            send_email_pool.set('sendemail:{}'.format(email), 1, ex=180)
    except Exception as e:
        raise self.retry(exc=e)
    return email


def parse_info(data, header=None, *args, **kwargs):
    """
    parser_info:
    param must be a dict
    parse dict data to json,and return HttpResponse
    """
    response = JsonResponse(data, *args, **kwargs)
    if header:
        response.set_cookie('access_token', header['access_token'])
    return response


def gen_jwt(user_id, user_email, do, exp_hours=1):
    jwt_payload = jwt.encode({
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=exp_hours),
        'user_id': user_id,
        'user_email': user_email,
        'do': do
    }, 'secret')

    return str(jwt_payload, encoding="utf-8")


def de_jwt(jwt_payload):
    try:
        return jwt.decode(jwt_payload, 'secret', leeway=1000)
    except Exception as e:
        raise e


def handle_post_body_to_json(func):
    def wrapper(*args, **kw):
        request = args[1]
        try:
            body = json.loads(request.body)
        except (json.decoder.JSONDecodeError):
            body = {i: request.POST.get(i) for i in request.POST.keys()}

        return func(*args, **kw, body = body)
    return wrapper


class CheckToken(object):
    token = None
    user = None

    def get_current_token(self):
        self.token = self.request.META.get('HTTP_AUTHORIZATION', '') or self.request.COOKIES.get('access_token',)
        return self.token

    def check_token(self):
        self.get_current_token()
        user = self.get_user_by_token()
        if user:
            self.user = user
            return True
        return False

    def wrap_check_token_result(self):
        result = self.check_token()
        if not result:
            self.message = 'Token 错误或过期，请重新登录'
            return False
        return True

    def get_user_by_token(self):
        try:
            payload = de_jwt(self.token)
        except Exception as e:
            return None

        user_id = payload['user_id']

        return User.get_user_by_id(user_id)


class Convert(Func):
    def __init__(self, expression, transcoding_name, **extra):
         super(Convert, self).__init__(
             expression, transcoding_name=transcoding_name, **extra)

    def as_mysql(self, compiler, connection):
        self.function = 'CONVERT'
        self.template = '%(function)s(%(expressions)s using %(transcoding_name)s)'
        return super(Convert, self).as_sql(compiler, connection)
