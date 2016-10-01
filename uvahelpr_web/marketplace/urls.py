from django.conf.urls import include, url
from django.contrib import admin

from . import views
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^jobs/$', views.allJobs, name='allJobs'),
    url(r'^home/$', views.home, name='home'),
]