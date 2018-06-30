from django.urls import path
from .views import *

urlpatterns = [
    path('auth/reg', RegUserView.as_view()),
    path('auth/login', LoginView.as_view()),
    path('auth/checkemail', check_email_view),

    path('user/profile', UserProfileView.as_view()),
    path('user/getapply', GetUserApplyView.as_view()),
    
    path('index/news/', NewsList.as_view()),
    path('index/hotvideo/', HotVideoListView.as_view()),
    path('index/recentevent/', RecentEvent.as_view()),

    path('event/', EventView.as_view()),
    path('event/getfilter', get_event_filter_view),
    path('event/detail/<str:id>', EventDetailView.as_view()),
    path('event/rules/<str:id>', EventRuleslView.as_view()),
    path('event/traffic/<str:id>', EventTrafficView.as_view()),
    path('event/sc/<str:id>', EventScView.as_view()),
    path('event/type/<str:event_id>', get_event_type_view),
    path('event/applyuser/<str:event_id>', get_event_apply_user_view),
    path('event/apply', ApplyUserView.as_view()),

    path('paragraph/user/', UserParagraphView.as_view()),
    path('paragraph/rzg/', RzgParagraphView.as_view()),
    path('paragraph/jl/', JlParagraphView.as_view()),

    path('score/user/', UserScoreView.as_view()),
    path('score/user/<str:user_id>', get_user_score_detail),
    path('score/event/', EventsScoreView.as_view()),
    # path('score/event/<str:user_id>', EventsScoreDetailView.as_view()),
    path('score/rank/', get_score_rank_view),
    # path('score/statistics/')

]