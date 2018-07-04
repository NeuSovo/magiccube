from django.contrib import admin
from django.urls import path, include
from . import views
from .router import *

urlpatterns = [
    path('recode/', include(DefaultRouter.router.urls))  # 视图集正常操作
]
