from django.urls import path
from .views import *

urlpatterns = [
    path('auth/reg', RegUserView.as_view()),
    path('auth/login', LoginView.as_view()),
    path('auth/checkemail', check_email_view),
    path('auth/forget', forget_password_view),
    path('auth/resendemail', resend_reg_email_view),

    path('user/profile', UserProfileView.as_view()),
    path('user/profile/<str:user_id>', get_user_profile_view),
    path('user/getapply', GetUserApplyView.as_view()),
    path('user/picture', UserPictureView.as_view()),
    path('user/resetpassword', ResetPasswordView.as_view()),
    path('user/avatar', UpdateUserAvatarView.as_view()),
    path('user/first', UserFirstView.as_view())
]