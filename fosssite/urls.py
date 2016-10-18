from django.conf.urls import url
from . import views
from django.conf.urls import  url

app_name = 'fosssite'
urlpatterns = [
	url(r'^$', views.home, name='home'),
	url(r'^signup/$', views.UserFormView, name='UserFormView'),
	url(r'^login/$',views.login_user,name='login_user'),
	url(r'^forgot_password/$', views.forgot_password, name='forgot_password'),
	url(r'^confirm_password/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', views.confirm_password, name='confirm_password'),
	url(r'^confirm_email/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', views.confirm_email, name='confirm_email'),
	url(r'signup_email/$', views.signup_email, name='signup_email'),
	url(r'^events/$',views.events,name='events'),
	url(r'^contributions/$',views.contributions,name='contributions'),
	url(r'^blog/$',views.blog,name='blog'),
	url(r'^logout/$',views.logout,name='logout'),
	url(r'^(?P<name>[\w\-]+)/$',views.profileuser,name='profileuser'),
	url(r'^(?P<name>[\w\-]+)/editprofile/$',views.edit_user_profile,name='edit_user_profile'),
	url(r'^(?P<name>[\w\-]+)/editprofile/changepassword/$',views.changepassword,name='changepassword'),
	url(r'^(?P<name>[\w\-]+)/editprofile/contributions/$',views.edit_contributions,name='edit_contributions'),
	url(r'^(?P<name>[\w\-]+)/editprofile/speakers/$',views.edit_speakers,name='edit_speakers'),


]
