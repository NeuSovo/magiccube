from django.urls import path
from .views import *

urlpatterns = [
    path('', get_project_view),
    path('<str:project_id>/', get_project_view),
]