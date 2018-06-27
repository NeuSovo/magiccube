import jwt
import json
import datetime
from celery.decorators import task

from django.http import JsonResponse
from django.core.mail import EmailMessage
from .apps import email_check_template

@task
def send_check_email(to_user, fail_silently=False):
    subject = 'test'
    to_list = [to_user.email]
    html_content = email_check_template.format(username=to_user.userprofile.username, token="http://127.0.0.1:8000/api/auth/checkemail?token="+gen_jwt(to_user.id, to_user.userprofile.username, 'checkemail'))
    msg = EmailMessage(subject, html_content, None, to_list)
    msg.content_subtype = "html"
    msg.send(fail_silently)
    to_user.is_email_check = 1
    to_user.save()


def handle_req(func):
    def wrapper(*args, **kwargs):
        request = args[0]
        try:
            body = json.loads(request.body)
        except Exception as e:
            return {'msg': 'error'}
        return func(*args, **kwargs, body=body)
    return wrapper


def parse_info(data):
    """
    parser_info:
    param must be a dict
    parse dict data to json,and return HttpResponse
    """
    return JsonResponse(data)


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
        return jwt.decode(jwt_payload, 'secret', leeway=10)
    except Exception as e:
        raise e
