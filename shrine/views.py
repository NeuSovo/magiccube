from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from .serializers import *
from .filters import *
from rest_framework import mixins
from rest_framework import generics
from rest_framework.decorators import detail_route
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend


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


class MiddleSet(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = test1.objects.all()
    serializer_class = TestSerializer

    @detail_route(methods=['get'], url_path='gets')
    def get(self, req, *args, **kwargs):
        return self.list(req, *args, **kwargs)


class TestViewSet(viewsets.ModelViewSet):
    queryset = test.objects.all()
    serializer_class = SnippetSerializer
    # filter_backends = (DjangoFilterBackend)
    # filter_fields = ('title',)


class Test1ViewSet(viewsets.ModelViewSet):
    queryset = test1.objects.all()
    serializer_class = TestSerializer
