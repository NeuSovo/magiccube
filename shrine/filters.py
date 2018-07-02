import django_filters
from django_filters.rest_framework import FilterSet as Set
from .models import *
from cms.models import *


class UserFilter(Set):
    name = django_filters.CharFilter(name="users__username")
    sex = django_filters.CharFilter(name="users__sex")
    area = django_filters.CharFilter(name="users__country")

    class Meta:
        model = User
        fields = ['id', 'name', 'sex', 'area']


class ContestFilter(Set):
    class Meta:
        model = Events
        fields = ['event_date', 'name', 'location', 'country', 'event_province', ]


class RankFilter(Set):
    area = django_filters.CharFilter(name='events__country')
    username = django_filters.CharFilter(name='username__username')
    events = django_filters.CharFilter(name='events__name')
    eventType = django_filters.CharFilter(name='eventType__type')
    sex = django_filters.CharFilter(name='username__sex')

    class Meta:
        model = Authority
        fields = ['username', 'area', 'events', 'eventType', 'sex']
