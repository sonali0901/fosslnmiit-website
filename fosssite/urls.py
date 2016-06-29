from django.conf.urls import url
from . import views
from django.conf.urls import patterns, url


urlpatterns = [
	url(r'^$', views.home, name='home'),
	url(r'^signup/', views.signup, name='signup'),
]
