import django_filters
from django_filters.rest_framework import FilterSet as Set
from .models import *
from utils.models import User
from event.models import Events


class UserFilter(Set):
    name = django_filters.CharFilter(name="userprofile__username", lookup_expr='icontains')
    sex = django_filters.CharFilter(name="userprofile__sex")
    area = django_filters.CharFilter(name="userprofile__country")
    id = django_filters.Filter(name='id', lookup_expr='contains')

    class Meta:
        model = User
        fields = ['id', 'name', 'sex', 'area']


class ContestFilter(Set):
    eventType = django_filters.CharFilter(name="eventtypedetail__type__type")
    name = django_filters.CharFilter(name='name', lookup_expr='icontains')
    location = django_filters.CharFilter(name='location', lookup_expr='icontains')

    class Meta:
        model = Events
        fields = ['event_date', 'country', 'eventType', 'name', 'location']


class RankFilter(Set):
    area = django_filters.CharFilter(name='events__country')
    # username = django_filters.CharFilter(name='username__username')
    # events = django_filters.CharFilter(name='events__name')
    eventType = django_filters.CharFilter(name='eventType__type')
    sex = django_filters.CharFilter(name='username__sex')

    class Meta:
        model = Authority
        fields = ['area', 'eventType', 'sex']
