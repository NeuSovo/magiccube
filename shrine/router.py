from .views import *
from rest_framework.routers import DefaultRouter


# todo 只有viewset 可以用路由 其他组合普通视图而已函数

class DefaultRouter:
    router = DefaultRouter()
    router.register('test', TestViewSet, base_name='nageshiurl')
    router.register('test1', Test1ViewSet)
    router.register('user', UserRecode)
