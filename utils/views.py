import requests
from django.http import QueryDict, Http404
from django.contrib.auth.hashers import make_password
from django.shortcuts import HttpResponseRedirect, render
from django.views.generic import (CreateView, FormView, ListView, UpdateView,
                                  View)
from django.core.validators import validate_email
from dss.Mixin import (FormJsonResponseMixin, JsonResponseMixin,
                       MultipleJsonResponseMixin)
from dss.Serializer import serializer

from event.models import ApplyUser
from .models import *
from .tools import *


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
        try:
            validate_email(email)
        except Exception as e:
            return self.render_to_response({'msg': '邮箱格式不符'})

        is_exist_user = User.get_user_by_email(email)
        if is_exist_user:
            # [TODO] 重发邮件
            return self.render_to_response({'msg': '已注册', 'email_status': is_exist_user.is_email_check})

        user = User.reg_user(email=email, username=username, password=password)
        if not send_email_pool.exists('sendemail:{}'.format(email)):
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

        if user.is_email_check != 2 :
            return self.render_to_response({'msg': '请先验证邮箱', 'is_email_check': user.is_email_check})

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


class UserPictureView(JsonResponseMixin, CheckToken, View):
    model = UserPicture

    def get(self, request, *args, **kwargs):
        if not self.wrap_check_token_result():
            return self.render_to_response({'msg': self.message})
        picture_list = self.user.userpicture_set.all()
        return parse_info({'picture_list': serializer(picture_list, exclude_attr=('user'))})

    def post(self, request, *args, **kwargs):
        if not self.wrap_check_token_result():
            return self.render_to_response({'msg': self.message})
        try:
            UserPicture(user=self.user, picture=request.FILES['img']).save()
            return self.get(request, *args, **kwargs)
        except Exception as e:
            return self.render_to_response({'msg': 'failed'})

    def delete(self, request, *args, **kwargs):
        if not self.wrap_check_token_result():
            return self.render_to_response({'msg': self.message})
        pid = QueryDict(request.body).get('pid')
        try:
            picture = UserPicture.objects.get(id=pid)
        except Exception as e:
            return self.render_to_response({'msg': 'failed'})

        picture.delete()
        return self.get(request, *args, **kwargs)


class UserFirstView(JsonResponseMixin, CheckToken, View):
    def get(self, request, *args, **kwargs):
        if not self.wrap_check_token_result():
            return self.render_to_response({'msg': self.message})
        picture_list = self.user.userfirst_set.all()
        return parse_info({'userfirst_list': serializer(picture_list, exclude_attr=('user','id'))})

    def post(self, request, *args, **kwargs):
        if not self.wrap_check_token_result():
            return self.render_to_response({'msg': self.message})
        try:
            # first_lists = request.POST.getlist('firsts')
            first_lists = (request.POST.get('firsts', '').split(','))
            self.user.userfirst_set.all().delete()
            to_save = [UserFirst(user=self.user, project=i) for i in first_lists]
            UserFirst.objects.bulk_create(to_save)
            return self.get(request, *args, **kwargs)
        except Exception as e:
            return self.render_to_response({'msg': 'failed'})


class ResetPasswordView(JsonResponseMixin, CheckToken, View):
    http_method_names = ['post', 'get']

    def get(self, request, *args, **kwargs):
        res = dict()
        jwt_payload = request.GET.get('token')
        try:
            print (jwt_payload)
            user_info = de_jwt(jwt_payload)
            user = User.get_user_by_id(user_info['user_id'])
            if user.email != user_info.get('user_email'):
                raise Exception("email error")
        except Exception as e:
            return parse_info({'msg': '连接可能失效或者过期 {}'.format(str(e))})

        if request.GET.get('password'):
            user.password = make_password(request.GET.get('password'))
            user.save()
            return parse_info({'msg': '重置成功'})
        
        return parse_info({'msg': '提交新密码'})

    @handle_post_body_to_json
    def post(self, request, body=None, *args, **kwargs):
        if not self.wrap_check_token_result():
            return self.render_to_response({'msg': self.message})
        old_password = body.get('password')
        new_password = body.get('new_password')
        if User.change_user_password(old_password, new_password, self.user):
            return parse_info({'msg': '修改成功'})
        return parse_info({'msg': '修改失败'})


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


class UpdateUserAvatarView(JsonResponseMixin, CheckToken, View):

    def post(self, request, *args, **kwargs):
        if not self.wrap_check_token_result():
            return self.render_to_response({'msg': self.message})
        try:
            self.user.userprofile.avatar = request.FILES['img']
            self.user.userprofile.save()
            return self.render_to_response({'msg': 'success', 'avatar': self.user.userprofile.avatar})
        except Exception as e:
            return self.render_to_response({'msg': 'failed:\t' + str(e)})


def check_email_view(request):
    res = dict()
    jwt_payload = request.GET.get('token')
    try:
        user_info = de_jwt(jwt_payload)
        user = User.get_user_by_id(user_info['user_id'])
    except Exception as e:
        return HttpResponseRedirect(FRONTEND_URL + '?check_success=0')

    if user.is_email_check == 2:
        return HttpResponseRedirect(FRONTEND_URL + '?check_success=1')

    user.is_email_check = 2
    user.save()

    access_token = gen_jwt(user_id=user.id, user_email=user.email, do="token")
    res['user_obj'] = serializer(
        user, exclude_attr=('password', 'id', 'reg_date'))
    res['msg'] = 'success'
    res['access_token'] = access_token

    return HttpResponseRedirect(FRONTEND_URL + '?check_success=1')


def forget_password_view(request):
    u_email = request.POST.get('email')
    if User.is_exist_user(u_email):
        if not send_email_pool.exists('sendemail:{}'.format(u_email)):
            forget_password_email.delay(u_email)
        return parse_info({'msg': '已向邮箱 {}发送一个修改链接，如果未收到可尝试在三分钟后重新提交'.format(u_email)})

    return parse_info({'msg': '邮箱不存在'})


def get_user_profile_view(request, user_id):
    res = {}
    try:
        user = User.get_user_by_id(user_id)
    except Exception as e:
        raise Http404('user_id 错误')
    res['profile'] = serializer(user.userprofile, exclude_attr=('user', 'phone', 'paperwork_type', 'paperwork_id'), datetime_format='string')
    res['picture'] = serializer(user.userpicture_set.all(), exclude_attr=('user'))
    res['apply_event'] = serializer(user.applyuser_set.all(), exclude_attr=('apply_user'), datetime_format='string')
    res['record'] = serializer(user.authority_set.all(), exclude_attr=('username','username_id','events_id','eventType_id',), datetime_format='string')

    return parse_info(res)


def resend_reg_email_view(request):
    email = request.GET.get('email')
    user = User.get_user_by_email(email)
    if not user:
        return parse_info({'msg': '邮箱不存在'})
    if not send_email_pool.exists('sendemail:{}'.format(email)):
        send_check_email.delay(uid=user.id, username=user.userprofile.username, email=email)

    return parse_info({'msg': "已向邮箱 {} 发送一封确认邮件".format(email)})


def wx_login_view(request):
    code = request.GET.get('code') or request.POST.get('code')
    is_mp = 'MicroMessenger' in request.META['HTTP_USER_AGENT']
    we = WeChatSdk(code=code, is_mp=is_mp)
    we_user_token = we.get_access_token()
    print (we_user_token)
    if 'errcode' in we_user_token:
        return parse_info(we_user_token)
    user_info = we.get_user_info(access_token=we_user_token['access_token'], openid=we_user_token['openid'])
    print (user_info)
    if WeChatUser.objects.filter(unionid=user_info['unionid']).exists():
        we_user = WeChatUser.objects.get(unionid=user_info['unionid'])
        we_user.update_profile(access_token=we_user_token['access_token'], refresh_token=we_user_token['refresh_token'], **user_info)
        resp = {}
        access_token = gen_jwt(
            user_id=we_user.user.id, user_email=we_user.user.email, do="token", exp_hours=24 * 7)
        resp['profile'] = serializer(
            we_user.user.userprofile, exclude_attr=('password', 'id', 'reg_date'))
        resp['access_token'] = access_token
        resp['expires_in'] = 3600 * 24 * 7
        return parse_info(resp)

    user = User.reg_user('微信用户', '填写你的姓名', 'default_password')
    we_user = WeChatUser(user=user)
    we_user.update_profile(access_token=we_user_token['access_token'], refresh_token=we_user_token['refresh_token'], **user_info)
    resp = {}
    access_token = gen_jwt(
        user_id=we_user.user.id, user_email=we_user.user.email, do="token", exp_hours=24 * 7)
    resp['profile'] = serializer(
        we_user.user.userprofile, exclude_attr=('password', 'id', 'reg_date'))
    resp['access_token'] = access_token
    resp['expires_in'] = 3600 * 24 * 7
    
    return parse_info(resp)
  
  
class BindWxView(JsonResponseMixin, View, CheckToken):

    def get(self, request, *args, **kwargs):
        if not self.wrap_check_token_result():
            return self.render_to_response({'msg': self.message})
        code = request.GET.get('code')
        is_mp = 'MicroMessenger' in request.META['HTTP_USER_AGENT']
        we = WeChatSdk(code=code, is_mp=is_mp)
        we_user_token = we.get_access_token()

        if 'errcode' in we_user_token:
            return self.render_to_response(we_user_token)
        user_info = we.get_user_info(access_token=we_user_token['access_token'], openid=we_user_token['openid'])
        if WeChatUser.objects.filter(unionid=user_info['unionid']).exists():
            return self.render_to_response({'msg': '该微信号已绑定其他账号'})

        we_user = WeChatUser(user=self.user)
        we_user.update_profile(access_token=we_user_token['access_token'], refresh_token=we_user_token['refresh_token'], **user_info)

        return self.render_to_response({'msg' : 'ok'})


class BindEmailView(JsonResponseMixin, View, CheckToken):

    def get(self, request, *args, **kwargs):
        token = request.GET.get('token')
        try:
            user_info = de_jwt(token)
            user = User.get_user_by_id(user_info['user_id'])
        except Exception as e:
            return parse_info({'msg': '连接可能失效或者过期 {}'.format(str(e))})

        user.is_email_check = 2
        user.email = user_info.get('user_email')
        user.save()
        return HttpResponseRedirect(FRONTEND_URL)


    @handle_post_body_to_json
    def post(self, request, body, *args, **kwargs):
        if not self.wrap_check_token_result():
            return self.render_to_response({'msg': self.message})

        email = body.get('email')
        try:
            validate_email(email)
        except Exception as e:
            return self.render_to_response({'msg': '邮箱格式不符'})

        is_exist_user = User.get_user_by_email(email)
        if is_exist_user:
            # [TODO] 重发邮件
            return self.render_to_response({'msg': '邮箱已被其他用户绑定', 'email_status': is_exist_user.is_email_check})

        bind_email_address.delay(uid=self.user.id, email=email)

        return self.render_to_response({'msg': "已向邮箱 {} 发送一封确认邮件".format(email)})
