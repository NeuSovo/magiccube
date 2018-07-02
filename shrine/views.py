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


class ContestRecode(viewsets.ReadOnlyModelViewSet):
    queryset = Events.objects.all()
    serializer_class = ContestRecodeX
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_class = ContestFilter


# class RankRecode(mixins.ListModelMixin, generics.GenericAPIView):
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

class RankRecode(viewsets.ReadOnlyModelViewSet):
    queryset = Authority.objects.all().order_by('single')
    serializer_class = RankRecodeX
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_class = RankFilter

    def get_queryset(self):
        queryset = Authority.objects.all().order_by('single')
        type = self.request.query_params
        return queryset

    @list_route(url_path='average')
    def average(self, request):
        pram = request.query_params
        if (pram['area']):
            queryset = Authority.objects.filter(username__username=pram['name'], events__country=pram['area'],
                                                events__name=pram['events']).order_by('single')
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        return Response('凉了,这个不会写')
class AuthorityRecode(viewsets.ReadOnlyModelViewSet):
    queryset = queryset = Authority.objects.all().order_by('single')
