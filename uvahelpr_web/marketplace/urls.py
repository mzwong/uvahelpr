from django.conf.urls import include, url
from django.contrib import admin

from . import views
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^jobs/(?P<id>[0-9]+)/$', views.job_entry, name="job_entry")
]