from django.conf.urls import include, url

from . import views
urlpatterns = [
    url(r'^v1/users/(?P<id>[0-9]+)/$', views.UserRU.as_view(), name="retrieve_update_users"),
    url(r'^v1/users/create/$', views.create_user, name="create_user"),
    url(r'^v1/users/delete/$', views.delete_user, name="delete_user"),
    url(r'^v1/jobs/$', views.get_all_jobs, name='get_all_jobs'),
    url(r'^v1/jobs/(?P<id>[0-9]+)/$', views.JobRU.as_view(), name="retrieve_update_jobs"),
    url(r'^v1/jobs/create/$', views.create_job, name="create_job"),
    url(r'^v1/jobs/delete/$', views.delete_job, name="delete_job"),
    url(r'^v1/messages/(?P<id>[0-9]+)/$', views.MessageRU.as_view(), name="retrieve_update_jobs"),
    url(r'^v1/messages/create/$', views.create_message, name="create_message"),
    url(r'^v1/messages/delete/$', views.delete_message, name="delete_message"),
    url(r'^v1/check_password/$', views.checkPassword, name="check_password"),
    url(r'^v1/create_authenticator/$', views.createAuthenticator, name="create_authenticator"),
    url(r'^v1/delete_authenticator/$', views.delete_authenticator, name="delete_authenticator"),
    url(r'^v1/auth_user/$', views.get_auth_user, name="auth_user"),
	url(r'^v1/create_job/$', views.create_job, name="create_job"),
]