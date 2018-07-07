from django.shortcuts import render
from dss.Mixin import FormJsonResponseMixin, MultipleJsonResponseMixin
from django.views.generic import FormView, CreateView, UpdateView, ListView
from .models import *
from dss.Serializer import serializer
from .tools import *
from event.models import ApplyUser

# Create your views here.
class RegUserView(FormJsonResponseMixin, CreateView):
    resp = dict()
    http_method_names = ['post']
    exclude_attr = ('form',)

    @handle_post_body_to_json
    def post(self, request, body=None, *args, **kwargs):
        # [TODO] check email style
        email = body.get('email')
        username = body.get('username')
        password = body.get('password')

        is_exist_user = User.get_user_by_email(email)
        if is_exist_user:
            # [TODO] 重发邮件
            return self.render_to_response({'msg': '已注册', 'email_status': is_exist_user.is_email_check})

        user = User.reg_user(email=email, username=username, password=password)
        send_check_email.delay(uid=user.id, username=username, email=email)
        self.resp['user_obj'] = serializer(
            user, exclude_attr=('password', 'id', 'reg_date'))
        self.resp['msg'] = "已向邮箱 {} 发送一封确认邮件".format(email)
        return self.render_to_response(self.resp)


class LoginView(FormJsonResponseMixin, FormView):
    http_method_names = ['post']
    resp = dict()

    @handle_post_body_to_json
    def post(self, request, body=None, *args, **kwargs):
        # user = User.login_user(request.POST.get(
        #     'email'), request.POST.get('password'))
        user = User.login_user(**body)
        if not user:
            return self.render_to_response({'msg': '账号或密码错误'})

        access_token = gen_jwt(
            user_id=user.id, user_email=user.email, do="token", exp_hours=24 * 7)
        self.resp['profile'] = serializer(
            user.userprofile, exclude_attr=('password', 'id', 'reg_date'))
        self.resp['access_token'] = access_token
        self.resp['expires_in'] = 3600 * 24 * 7

        response = self.render_to_response(self.resp)
        response.set_cookie('access_token', access_token)
        return response


class UserProfileView(FormJsonResponseMixin, CheckToken, UpdateView):
    model = UserProfile

    def get(self, request, *args, **kwargs):
        if not self.wrap_check_token_result():
            return self.render_to_response({'msg': self.message})

        return self.render_to_response(serializer(self.user.userprofile, exclude_attr=('password', 'id', 'reg_date')))

    @handle_post_body_to_json
    def post(self, request, body=None, *args, **kwargs):
        if not self.wrap_check_token_result():
            return self.render_to_response({'msg': self.message})
        self.user.userprofile.update(**body)
        return self.render_to_response(serializer(self.user.userprofile, exclude_attr=('password', 'id', 'reg_date')))


class GetUserApplyView(MultipleJsonResponseMixin, CheckToken, ListView):
    model = ApplyUser
    exclude_attr = ('password', 'id', 'event_id', 'reg_date', 'apply_user', 'evnet_weight',
                    'event_province', 'event_province_id', 'event_project', 'event_project_id')

    def get_queryset(self):
        if not self.wrap_check_token_result():
            return self.render_to_response({'msg': self.message})
        queryset = super(GetUserApplyView, self).get_queryset()

        queryset = queryset.filter(apply_user=self.user)
        return queryset


def check_email_view(request):
    res = dict()
    jwt_payload = request.GET.get('token')
    try:
        user_info = de_jwt(jwt_payload)
        user = User.get_user_by_id(user_info['user_id'])
    except Exception as e:
        return parse_info({'msg': '连接可能失效或者过期'})

    if user.is_email_check == 2:
        return parse_info({'msg': '已验证'})

    user.is_email_check = 2
    user.save()

    access_token = gen_jwt(user_id=user.id, user_email=user.email, do="token")
    res['user_obj'] = serializer(
        user, exclude_attr=('password', 'id', 'reg_date'))
    res['msg'] = 'success'
    res['access_token'] = access_token

    return parse_info(res, header={'access_token': access_token})