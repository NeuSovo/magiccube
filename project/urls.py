from django.urls import path
from .views import *

urlpatterns = [
    path('project', get_project_view),
    path('ssz', get_ssz_view),
]