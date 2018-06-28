import jwt
import json
import datetime
from celery.decorators import task

from django.http import JsonResponse
from django.core.mail import EmailMessage
from .apps import email_check_template
from .models import User

@task
def send_check_email(to_user, fail_silently=False):
    subject = 'test'
    to_list = [to_user.email]
    token = "http://127.0.0.1:8000/api/auth/checkemail?token="+gen_jwt(to_user.id, to_user.userprofile.username, 'checkemail')
    html_content = email_check_template.format(username=to_user.userprofile.username, token=token)
    msg = EmailMessage(subject, html_content, None, to_list)
    msg.content_subtype = "html"
    msg.send(fail_silently)
    to_user.is_email_check = 1
    to_user.save()


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


def gen_jwt(user_id, user_email, do,exp_hours=1):
    jwt_payload = jwt.encode({
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=exp_hours),
        'user_id': user_id,
        'user_email': user_email,
        'do': do
    }, 'secret')

    return str(jwt_payload, encoding="utf-8")


def de_jwt(jwt_payload):
    try:
        return jwt.decode(jwt_payload, 'secret', leeway=10000)
    except Exception as e:
        raise e


class CheckToken(object):
    token = None
    user = None

    def get_current_token(self):
        self.token = self.request.POST.get('access_token', '') or self.request.COOKIES.get('access_token',)
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
