from django.contrib import admin
from django.urls import path, include
from . import views
from .router import *

urlpatterns = [
    path(r'snippets', views.snippet_list),
    path(r'snippets/<int:pk>', views.snippet_detail),
    path('middle', views.MiddleSet.as_view()),  # 普通视图演示
    path('test', views.TestViewSet.as_view(  # 视图集不推荐写法
        {'get': 'list'}
    )),
    path('router/', include(DefaultRouter.router.urls))  # 视图集正常操作
]
