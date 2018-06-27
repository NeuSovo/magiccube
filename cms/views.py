# -*- coding: utf-8 -*-
from dss.Mixin import MultipleJsonResponseMixin, JsonResponseMixin
from dss.Serializer import serializer

from django.shortcuts import render
from django.views.generic import ListView, DetailView

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


class EventView(MultipleJsonResponseMixin, ListView):
    model = Events
    query_set = Events.objects.all()
    paginate_by = 15
    datetime_type = 'string'
    # foreign = True
    exclude_attr = ('event_year', 'event_year_id', 'event_province_id', 'event_project', 'event_project_id')

    def get_queryset(self):
        kwargs = {
        }
        year = self.request.GET.get('year', None)
        type_ = self.request.GET.get('type', None)
        province = self.request.GET.get('province', None)
        project = self.request.GET.get('project', None)

        if year: kwargs['event_date__year'] = year
        if province: kwargs['event_province_id'] = province
        if project: kwargs['event_project_id'] = project
        if type_:kwargs['eventtypedetail__type'] = type_

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


class HotVideoListView(MultipleJsonResponseMixin, ListView):
    model = HotVideo
    query_set = HotVideo.objects.all()
    paginate_by = 15
    datetime_type = 'string'


@handle_req
def reg_view(request, body):
    res = dict()

    if User.is_exist_user(body.get('email')):
        return parse_info({'meg': '已注册'})

    user = User.reg_user(body=body)
    if not user:
        return parse_info({"msg": 'error'})     #

    send_check_email(to_user=user)
    res['user_obj'] =  serializer(user, exclude_attr=('password', 'id', 'reg_date'))
    res['msg'] = '已发送邮箱链接,,,'

    return parse_info(res)
    

@handle_req
def login_view(request, body):
    res = dict()
    user = User.login_user(body=body)
    if not user:
        return parse_info({"msg": '账号或密码错误'})

    if user.is_email_check == 1:
        return parse_info({'msg': '请先验证邮箱'})

    res['user_obj'] = serializer(user, exclude_attr=('password', 'id', 'reg_date'))
    res['jwt_token'] = gen_jwt(user_id=user.id, user_email=user.email, do="token")

    return parse_info(res)


def check_email_view(request):
    res = dict()
    jwt_payload = request.GET.get('token')
    try:
        user_info = de_jwt(jwt_payload)
    except:
        return parse_info({'msg': '连接可能失效或者过期'})

    if user.is_email_check == 2:
        return parse_info({'msg': '已验证'})

    user = User.get_user_by_id(user_info['user_id'])
    user.is_email_check = 2
    user.save()

    res['user_obj'] =  serializer(user, exclude_attr=('password', 'id', 'reg_date'))
    res['msg'] = 'success'
    res['jwt_token'] = gen_jwt(user_id=user.id, user_email=user.email, do="token")

    return parse_info(res)


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
    queryset = EventTypeDetail.objects.filter(event_id = event_id)
    all_type = []
    for i in queryset:
        all_type.append({
            'id': i.id,
            'type_name': i.type.type,
            'type_lines': i.lines,
            'type_price': i.price
            })

    res['type'] = all_type
    event = Events.objects.get(id=event_id)
    res['can_apply_count'] = int(event.eventsdetail.apply_count) - len(event.applyuser_set.filter(is_check=1))

    return parse_info(res)
    