from django.conf.urls import include, url
from django.contrib import admin

from . import views
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^jobs/(?P<id>[0-9]+)/$', views.job_entry, name="job_entry"),
    url(r'^jobs/$', views.allJobs, name='allJobs'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
]