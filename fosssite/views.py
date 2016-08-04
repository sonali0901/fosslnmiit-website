from django.views.generic import View
from django.utils import timezone
from django.shortcuts import render, get_object_or_404,render_to_response,redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
#from django.core.context_processors import csrf
#from django.views.decorators import csrf
from passlib.hash import pbkdf2_sha256
from .forms import UserForm

# Create your views here.

def home(request):
	if request.user.is_authenticated():
		return redirect('fosssite:profileuser')
	return render(request, 'fosssite/home.html')

def login_user(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username,password=password)
		if user is not None:
			auth.login(request, user)
			#return render(request, 'fosssite/profileuser.html', {'username': user.username})
			return redirect('fosssite:profileuser')
		else:
			return render(request, 'fosssite/login.html', {'error_message': 'Invalid login'})
	return render(request,'fosssite/login.html')


def UserFormView(request):
	form=UserForm(request.POST or None)
	if form.is_valid():
		# not saving to database only creating object
		user=form.save(commit=False)
		#normalized data
		user.first_name = form.data['fname']
		user.last_name = form.data['lname']
		username=form.cleaned_data['username']
		password=form.cleaned_data['password']
		#not as plain data
		#password=pbkdf2_sha256.encrypt(text_password,rounds=12000,salt_size=32)
		user.set_password(password)
		user.save() #saved to database
		user = auth.authenticate(username=username,password=password)
		if user is not None:
			auth.login(request, user)
			return redirect('fosssite:profileuser')
	return render(request,'fosssite/signup.html',{'form':form})
"""
def auth_view(request):
	username=request.POST.get('username', '')
	password=request.POST.get('password', '')
	user=auth.authenticate(username=username,password=password)

	if user is not None:
		auth.login(request,user)
		return HttpResponseRedirect('/profileuser')#url in brackets
	else:
		return HttpResponseRedirect('/invalid')
"""
def profileuser(request):
	#url = request.user.profile.url
	return render(request,'fosssite/profileuser.html',{'username':request.user.username})

def logout(request):
	auth.logout(request)
	return HttpResponseRedirect('/')

def edit_user_profile(request):
	return  render_to_response('fosssite/edituser.html')
"""
def invalid_login(request):
	return render_to_response('fosssite/invalid_login.html')

def view_profile(request):
    url = request.user.profile.url
"""
