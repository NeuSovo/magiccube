from django.urls import path
from .views import *

urlpatterns = [
    path('auth/reg', RegUserView.as_view()),
    path('auth/login', LoginView.as_view()),
    path('auth/checkemail', check_email_view),

    path('user/profile', UserProfileView.as_view()),
    path('user/getapply', GetUserApplyView.as_view()),
]