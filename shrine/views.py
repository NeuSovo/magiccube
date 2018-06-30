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


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """

    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


def snippet_list(request):
    """
    列出所有的code snippet，或创建一个新的snippet。
    """
    if request.method == 'GET':
        snippets = test.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)


def snippet_detail(request, pk):
    """
    获取，更新或删除一个 code snippet。
    """
    try:
        snippet = test.objects.get(id=int(pk))
        print(snippet)
    except test.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = SnippetSerializer(snippet)
        return JSONResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(snippet, data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        return JSONResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        snippet.delete()
        return HttpResponse(status=204)


# class MiddleSet(mixins.ListModelMixin, generics.GenericAPIView):
class MiddleSet(generics.ListAPIView):
    queryset = test1.objects.all()
    serializer_class = TestSerializer


class TestViewSet(viewsets.ModelViewSet):
    queryset = test.objects.all()
    serializer_class = SnippetSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_class = TestFilter

    # def list(self, request, *args, **kwargs):
    #     return Response({'status': 'password set'})


class Test1ViewSet(viewsets.ModelViewSet):
    queryset = test1.objects.all()
    serializer_class = TestSerializer


class UserRecode(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserRecodeX
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_class = UserFilter

    # def get_queryset(self):
    #     queryset = User.objects.all()
    #     username = self.request.query_params.get('name', None)
    #     area = self.request.query_params.get('area', None)
    #     sex = self.request.query_params.get('sex', None)
    #     if username or area or sex is not None:
    #         queryset = queryset.filter(purchaser__username=username)
    #     return queryset

    # @list_route(url_path='user')
    # def get_user(self, request, pk=None):
    #     def list(self, request, *args, **kwargs):
    #         queryset = self.filter_queryset(self.get_queryset())
    #
    #         page = self.paginate_queryset(queryset)
    #         if page is not None:
    #             serializer = self.get_serializer(page, many=True)
    #             return self.get_paginated_response(serializer.data)
    #
    #         serializer = self.get_serializer(queryset, many=True)
    #         return Response(serializer.data)
    #     return Response('user')


class ContestRecode(viewsets.ReadOnlyModelViewSet):
    queryset = Events.objects.all()
    serializer_class = ContestRecodeX
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_class = ContestFilter
