from django.shortcuts import render
from dss.Mixin import MultipleJsonResponseMixin
from django.views.generic import ListView
from dss.Serializer import serializer
from index.models import *
from event.models import Events
from utils.tools import parse_info

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


def get_join_our(request):
    info = JoinOur.objects.all()[:1]
    if info:
        return parse_info({'info': info[0].info})
    return parse_info({})


def get_lunbo_img(request):
    count = request.GET.get('count', 3)
    lists = LunBo.objects.all()[:count]
    if lists:
        return parse_info({'list': serializer(lists)})
    return parse_info({})
