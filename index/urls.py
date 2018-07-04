from django.urls import path
from .views import *

urlpatterns = [
    path('news/', NewsList.as_view()),
    path('hotvideo/', HotVideoListView.as_view()),
    path('recentevent/', RecentEvent.as_view()),
]