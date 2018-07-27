from django.urls import path
from .views import *
from weixin import Weixin, WeixinError


config = dict(WEIXIN_APP_ID='wxb4ded851965b77eb', WEIXIN_APP_SECRET='5c4a6e4a8f8aa560dd8c3eff6536576f')
weixin = Weixin(config)

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
    path('user/first', UserFirstView.as_view()),

    path('wx/', weixin.django_view_func())
]