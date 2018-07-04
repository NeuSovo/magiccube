from .models import *
from dss.Mixin import MultipleJsonResponseMixin, JsonResponseMixin, FormJsonResponseMixin
from dss.Serializer import serializer

from django.http import Http404
from django.views.generic import ListView, DetailView, FormView, CreateView, UpdateView
from utils.tools import CheckToken, parse_info

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
