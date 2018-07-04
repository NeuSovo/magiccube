from django.urls import path
from .views import *
urlpatterns = [
    path('user/', UserParagraphView.as_view()),
    path('rzg/', RzgParagraphView.as_view()),
    path('jl/', JlParagraphView.as_view())
]