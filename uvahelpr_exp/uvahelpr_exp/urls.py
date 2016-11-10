"""uvahelpr_exp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from . import views
urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', views.login, name='login'),
    url(r'^auth-user/$', views.getAuthUser, name='auth_user'),
    url(r'^create_account/$', views.create_account, name='create_account'),
    url(r'^jobs/$', views.get_all_jobs, name='get_all_jobs'),
    url(r'^jobs/(?P<id>[0-9]+)/$', views.job_summary, name='get_job'),
    url(r'^logout/$', views.logout, name='logout'),
	url(r'^create_job/$', views.create_job, name='create_job'),
    url('r^search/$', views.search_listing, name='search_listing')
]
