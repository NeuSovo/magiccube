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
