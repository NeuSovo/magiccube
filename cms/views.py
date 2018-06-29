# -*- coding: utf-8 -*-
from dss.Mixin import MultipleJsonResponseMixin, JsonResponseMixin, FormJsonResponseMixin
from dss.Serializer import serializer

from django.http import Http404
from django.shortcuts import render
from django.views.generic import ListView, DetailView, FormView, CreateView, UpdateView, View
from django.db.models import Q

from .models import *
from .tasks import *


class NewsList(MultipleJsonResponseMixin, ListView):
    model = News
    query_set = News.objects.all()
    paginate_by = 15
    datetime_type = 'string'


class RecentEvent(MultipleJsonResponseMixin, ListView):
    model = Events
    query_set = Events.objects.all()[:15]
    paginate_by = 15
    datetime_type = 'string'


class HotVideoListView(MultipleJsonResponseMixin, ListView):
    model = HotVideo
    query_set = HotVideo.objects.all()[:15]
    paginate_by = 15
    datetime_type = 'string'


class EventView(MultipleJsonResponseMixin, ListView):
    model = Events
    paginate_by = 15
    datetime_type = 'string'
    exclude_attr = ('event_year', 'event_year_id',
                    'event_province_id', 'event_project', 'event_project_id')

    def get_queryset(self):
        kwargs = {
        }
        year = self.request.GET.get('year', None)
        type_ = self.request.GET.get('type', None)
        province = self.request.GET.get('province', None)
        project = self.request.GET.get('project', None)

        if year:
            kwargs['event_date__year'] = year
        if province:
            kwargs['event_province_id'] = province
        if project:
            kwargs['event_project_id'] = project
        if type_:
            kwargs['eventtypedetail__type'] = type_

        queryset = super(EventView, self).get_queryset()
        queryset = queryset.filter(**kwargs)
        return queryset


class EventDetailView(JsonResponseMixin, DetailView):
    model = EventsDetail
    foreign = True
    many = True
    datetime_type = 'string'
    pk_url_kwarg = 'id'
    exclude_attr = ('id_id',)


class EventRuleslView(JsonResponseMixin, DetailView):
    model = EventRules
    foreign = True
    many = True
    datetime_type = 'string'
    pk_url_kwarg = 'id'
    exclude_attr = ('id_id',)


class EventTrafficView(JsonResponseMixin, DetailView):
    model = EventTraffic
    foreign = True
    many = True
    datetime_type = 'string'
    pk_url_kwarg = 'id'
    exclude_attr = ('id_id',)


class EventScView(JsonResponseMixin, DetailView):
    model = EventSc
    foreign = True
    many = True
    datetime_type = 'string'
    pk_url_kwarg = 'id'
    exclude_attr = ('id_id',)


class ApplyUserView(FormJsonResponseMixin, CheckToken, FormView):
    model = ApplyUser

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates a blank version of the form.
        """
        return parse_info({'msg': 'token'})

    def post(self, request, *args, **kwargs):
        if not self.wrap_check_token_result():
            return self.render_to_response({'msg': self.message})

        if ApplyUser.objects.filter(apply_user=self.user).exists():
            return parse_info({'msg': '已报名'})

        for i in request.POST.keys():
            kwargs[i] = request.POST[i]
        apply_types = request.POST.getlist('types')
        apply_ = ApplyUser.create(
            user=self.user, apply_types=apply_types, **kwargs)
        return self.render_to_response(serializer(apply_, exclude_attr=('password', 'id', 'reg_date'), datetime_format='string'))


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


class RegUserView(FormJsonResponseMixin, CreateView):
    resp = dict()
    http_method_names = ['post']
    exclude_attr = ('form',)

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')

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

    def post(self, request, *args, **kwargs):
        user = User.login_user(request.POST.get(
            'email'), request.POST.get('password'))
        if not user:
            return self.render_to_response({'msg': '账号或密码错误'})

        access_token = gen_jwt(
            user_id=user.id, user_email=user.email, do="token", exp_hours=72)
        self.resp['profile'] = serializer(
            user.userprofile, exclude_attr=('password', 'id', 'reg_date'))
        self.resp['access_token'] = access_token

        response = self.render_to_response(self.resp)
        response.set_cookie('access_token', access_token)
        return response


class UserProfileView(FormJsonResponseMixin, CheckToken, UpdateView):
    model = UserProfile

    def get(self, request, *args, **kwargs):
        if not self.wrap_check_token_result():
            return self.render_to_response({'msg': self.message})

        return self.render_to_response(serializer(self.user.userprofile, exclude_attr=('password', 'id', 'reg_date')))

    def post(self, request, *args, **kwargs):
        if not self.wrap_check_token_result():
            return self.render_to_response({'msg': self.message})

        for i in request.POST.keys():
            kwargs[i] = request.POST[i]

        self.user.userprofile.update(**kwargs)
        return self.render_to_response(serializer(self.user.userprofile, exclude_attr=('password', 'id', 'reg_date')))


class UserParagraphView(MultipleJsonResponseMixin, ListView):
    model = UserParagraph
    paginate_by = 15
    datetime_type = 'string'

    exclude_attr = ('password','is_email_check', 'reg_date', 'rz_date', 'email', 'phone', 'paperwork_type', 'paperwork_id')


    def get_queryset(self):
        search = self.request.GET.get('search', None)
        queryset = super(UserParagraphView, self).get_queryset()
        if search:
            queryset = queryset.filter(Q(paragraph__contains=search) | Q(user__username__contains=search) | Q(user__country__contains=search))

        return queryset


class RzgParagraphView(MultipleJsonResponseMixin, ListView):
    model = RzgParagraph
    paginate_by = 15
    datetime_type = 'string'

    def get_queryset(self):
        search = self.request.GET.get('search', None)
        queryset = super(RzgParagraphView, self).get_queryset()
        if search:
            queryset = queryset.filter(Q(country__contains=search) | Q(name__contains=search))

        return queryset


class JlParagraphView(MultipleJsonResponseMixin, ListView):
    model = JlParagraph
    paginate_by = 15
    datetime_type = 'string'

    def get_queryset(self):
        search = self.request.GET.get('search', None)
        queryset = super(JlParagraphView, self).get_queryset()
        if search:
            queryset = queryset.filter(Q(country__contains=search) | Q(name__contains=search) | Q(paragraph__contains=search))

        return queryset


class UserScoreView(MultipleJsonResponseMixin, ListView):
    model = UserProfile
    paginate_by = 15
    datetime_type = 'string'

    exclude_attr = ('password','is_email_check', 'reg_date', 'rz_date', 'email', 'phone', 'paperwork_type', 'paperwork_id','event')


# class UserScoreDetailView(JsonResponseMixin, View):
#     model = UserScore
#     pk_url_kwarg = 'user_id'
#     foreign = True

#     def get_queryset(self):
#         if self.queryset is None:
#             if self.model:
#                 return self.model._default_manager.all()
#             else:
#                 raise ImproperlyConfigured(
#                     "%(cls)s is missing a QuerySet. Define "
#                     "%(cls)s.model, %(cls)s.queryset, or override "
#                     "%(cls)s.get_queryset()." % {
#                         'cls': self.__class__.__name__
#                     }
#                 )
#         pk = self.kwargs.get('pk_url_kwarg')
#         queryset =  self.queryset.all()
#         if pk is not None:
#             queryset = queryset.filter(user__id=pk)
#         return queryset



class EventsScoreView(MultipleJsonResponseMixin, ListView):
    model = Events
    paginate_by = 15
    datetime_type = 'string'


class EventsScoreDetailView(JsonResponseMixin, DetailView):
    pass


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


def get_event_filter_view(request):
    res = dict()
    all_project = EventProject.objects.all()
    all_province = EventProvince.objects.all()
    all_type = EventType.objects.all()

    res['all_project'] = serializer(all_project)
    res['all_province'] = serializer(all_province)
    res['all_type'] = serializer(all_type)

    return parse_info(res)


def get_event_type_view(request, event_id):
    res = dict()
    try:
        event = Events.objects.get(id=event_id)
        queryset = EventTypeDetail.objects.filter(event=event)
    except Exception as e:
        raise Http404("event_id：{} 错误".format(event_id))

    all_type = []
    for i in queryset:
        all_type.append({
            'id': i.id,
            'type_name': i.type.type,
            'type_lines': i.lines,
            'type_price': i.price
        })

    res['type'] = all_type
    
    res['can_apply_count'] = int(
        event.eventsdetail.apply_count) - len(event.applyuser_set.filter(is_check=1))

    return parse_info(res)


def get_event_apply_user_view(request, event_id):
    res = dict()
    try:
        event = Events.objects.get(id=event_id)
        queryset = event.applyuser_set.filter(is_check=0)
    except Exception as e:
        raise Http404("event_id：{} 错误".format(event_id))

    apply_list = []
    for i in queryset:
        apply_list.append({
            'user_obj': {
                'id': i.apply_user.id,
                'username': i.apply_user.userprofile.username,
                'sex': i.apply_user.userprofile.sex or '',
            },
            'apply_types': [i.apply_type.type.type for i in i.applyusertypes_set.all()],
            'apply_time': i.create_time
        })
    res['list'] = apply_list
    return parse_info(res, safe=True)


def get_user_score_detail(request, user_id):
    res = dict()
    try:
        user = User.objects.get(id=user_id)
    except Exception as e:
        raise Http404("user_id {} 错误".format(user_id))

    queryset = UserScore.objects.filter(user=user.userprofile)
    res['user_obj'] = serializer(user.userprofile, exclude_attr=('user', 'phone', 'paperwork_type', 'paperwork_id'))

    score_detail = []

    for i in queryset:
        score_detail.append(serializer(i.scoretypes_set.all(), exclude_attr=('detail')))

    res['score_detail'] = score_detail
    return parse_info(res)