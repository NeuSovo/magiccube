from .views import *
from rest_framework.routers import DefaultRouter


class DefaultRouter:
    router = DefaultRouter()
    router.register(r'users', TestViewSet, base_name='user')
    router.register('test1', Test1ViewSet)
