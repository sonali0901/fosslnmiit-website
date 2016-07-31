from django.conf.urls import url
from . import views
from django.conf.urls import patterns, url


urlpatterns = [
	url(r'^$', views.home),
	url(r'^signup/$', views.UserFormView),
	url(r'^login/$',views.login),
	url(r'^auth/$',views.auth_view),
	url(r'^profileuser/$',views.loggedin),
	url(r'^edituser/$',views.edit_user_profile),
]
