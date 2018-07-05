"""magiccube URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('utils.urls')),
    path('api/index/', include('index.urls')),
    path('api/event/', include('event.urls')),
    path('api/paragraph/', include('paragraph.urls')),
    path('api/', include('shrine.urls')),
    path('api/project/', include('project.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
