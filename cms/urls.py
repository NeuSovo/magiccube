from django.urls import path
from .views import *

urlpatterns = [
    path('auth/reg', reg_view),
    path('auth/login', login_view),
    path('auth/checkemail', check_email_view),

    path('index/news/', NewsList.as_view()),
    path('index/event/recent/', RecentEvent.as_view()),
    path('index/hotvideo/', HotVideoListView.as_view()),

    path('event/', EventView.as_view()),
    path('event/getfilter', get_event_filter_view),
    path('event/detail/<str:id>', EventDetailView.as_view())
]