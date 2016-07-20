from django.utils import timezone
from django.shortcuts import render, get_object_or_404,render_to_response,redirect
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.core.context_processors import csrf

# Create your views here.

def home(request):
	return render(request, 'fosssite/home.html')
def signup(request):
	return render(request,'fosssite/signup.html')
def login(request):
	c={}
	c.update(csrf(request))
	return render_to_response('fosssite/login.html',c)

def auth_view(request):
	username=request.POST.get('username', '')
	password=request.POST.get('password', '')
	user=auth.authenticate(username=username,password=password)

	if user is not None:
		auth.login(request,user)
		return HttpResponseRedirect('/loggedin')#url in brackets
	else:
		return HttpResponseRedirect('/invalid')

def loggedin(request):
	return render_to_response('fosssite/loggedin.html',{'fullname':request.user.username})

def logout(request):
	auth.logout(request)
	return render_to_response('fosssite/logout.html')

def invalid_login(request):
	return render_to_response('fosssite/invalid_login.html')