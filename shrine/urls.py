from django.contrib import admin
from django.urls import path
from . import views



urlpatterns = [
    path(r'snippets', views.snippet_list),
    path(r'snippets/<int:pk>', views.snippet_detail),
]
