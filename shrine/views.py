from django.http import HttpResponse

from .serializers import *
from .filters import *

import django_filters.rest_framework

from rest_framework import mixins
from rest_framework import generics
from rest_framework.decorators import *
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser


class UserRecode(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserRecodeX
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_class = UserFilter
    pagination_class = CommonPagination


class ContestRecode(viewsets.ReadOnlyModelViewSet):
    queryset = Events.objects.all()
    serializer_class = ContestRecodeX
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_class = ContestFilter
    pagination_class = CommonPagination


class RankRecode(viewsets.ReadOnlyModelViewSet):
    queryset = Authority.objects.all().order_by('single')
    serializer_class = RankRecodeX
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_class = RankFilter
    pagination_class = CommonPagination

    def get_queryset(self):
        queryset = Authority.objects.all().order_by('single')
        type = self.request.query_params
        return queryset

    def authority(self, area):
        type = EventType.objects.all()
        list = []
        for i in type:
            exists = Authority.objects.filter(eventType__type=i, events__country=area).exists()
            data = Authority.objects.filter(eventType__type=i, events__country=area).order_by('single').first()
            if (exists):
                serializer = RankRecodeX(data)
                list.append(serializer.data)
        return Response(list)

    @list_route(url_path='authority')
    @renderer_classes((JSONRenderer,))
    def average(self, request):
        area = request.query_params.get('area', None)
        NULL = {'msg': 'not data'}
        if (area):
            return (self.authority(area))
        return Response(NULL)
