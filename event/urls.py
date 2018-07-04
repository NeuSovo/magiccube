from django.urls import path
from .views import *

urlpatterns = [
    path('', EventView.as_view()),
    path('getfilter/', get_event_filter_view),
    path('detail/<str:id>', EventDetailView.as_view()),
    path('rules/<str:id>', EventRuleslView.as_view()),
    path('traffic/<str:id>', EventTrafficView.as_view()),
    path('sc/<str:id>', EventScView.as_view()),
    path('type/<str:event_id>', get_event_type_view),
    path('applyuser/<str:event_id>', get_event_apply_user_view),
    path('apply/', ApplyUserView.as_view()),
]