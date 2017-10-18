"""klaviyo_weather_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include,url
from django.contrib import admin
import os
from rest_framework import routers
import sys
from klaviyo_weather_api import views
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
from django.core.wsgi import get_wsgi_application

SYS_PATH = os.path.dirname(BASE_DIR)
print SYS_PATH
if SYS_PATH not in sys.path:
    sys.path.append(SYS_PATH)
os.environ['DJANGO_SETTINGS_MODULE'] = 'user_profile_backend.settings'
application = get_wsgi_application()



urlpatterns = [
    url(r'^admin/', admin.site.urls),
]
router = routers.DefaultRouter()
router.register(r'users', views.UserList, 'list')
router.register(r'cities', views.CityList, 'list')
urlpatterns = [
    url(r'^klaviyo-weather/api/', include(router.urls)),
    url(r'^klaviyo-weather/api/messages', views.UserMessage.as_view()),
    url(r'^klaviyo-weather/api/sendEmail', views.EmailAPI.as_view()),
    ]