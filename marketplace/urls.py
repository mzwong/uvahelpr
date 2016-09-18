from django.conf.urls import include, url
from django.contrib import admin

from . import views
urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^v1/users/(?P<id>[0-9]+)/$', views.UserRU.as_view(), name="retrieve_update_users"),
	url(r'^v1/users/create/$', views.create_user, name="create_user"),
	url(r'^v1/users/delete/$', views.delete_user, name="delete_user")
]