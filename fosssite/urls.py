from django.conf.urls import url
from . import views
from django.conf.urls import  url

app_name = 'fosssite'
urlpatterns = [
	url(r'^$', views.home, name='home'),
	url(r'^signup/$', views.UserFormView, name='UserFormView'),
	url(r'^login/$',views.login_user,name='login_user'),
	#url(r'^auth/$',views.auth_view,name='auth_view'),
	url(r'^profileuser/$',views.profileuser,name='profileuser'),
	url(r'^logout/$',views.logout,name='logout'),
	url(r'^edit_user_profile/$',views.edit_user_profile,name='edit_user_profile'),
]
