from django.shortcuts import render
from dss.Mixin import MultipleJsonResponseMixin
from django.views.generic import ListView

from index.models import *
from event.models import Events

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