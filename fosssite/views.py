from django.views.generic import View
from django.utils import timezone
from django.shortcuts import render, get_object_or_404,render_to_response,redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
#from django.core.context_processors import csrf
#from django.views.decorators import csrf
#from passlib.hash import pbkdf2_sha256
from .forms import UserForm, UserProfileForm, UserEditForm
from .models import UserProfile
#from django.views.generic.edit import UpdateView
# Create your views here.

def home(request):
	if request.user.is_authenticated():
		return redirect('fosssite:profileuser')
	return render(request, 'fosssite/home.html')

def login_user(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
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
@login_required
def profileuser(request):
	#url = request.user.profile.url
	return render(request,'fosssite/profileuser.html',{'username':request.user.username})

def logout(request):
	auth.logout(request)
	return HttpResponseRedirect('/')

@login_required
def edit_user_profile(request):
	#print request.user
	if request.method == 'POST':
		profile_form = UserProfileForm(data=request.POST)
		user_form = UserEditForm(data=request.POST, instance=request.user)
		if user_form.is_valid() and profile_form.is_valid():

			user = user_form.save(commit=False)
			user.email = request.POST.get('user[email]')
			user.first_name = request.POST.get('user[fname]')
			user.last_name = request.POST.get('user[lname]')
			password = request.POST.get('user[password]')
			user.set_password(password)
			#user,username is missing here.

			profile = profile_form.save(commit=False)
			profile.user = request.user
			print profile.user
			profile.handle = request.POST.get('user[handle]')
			profile.about_me = request.POST.get('user[about_me]')
			profile.twitterurl = request.POST.get('user[twitter_handle]')
			profile.facebookurl = request.POST.get('user[facebook_profile]')
			profile.lnkdnurl = request.POST.get('user[linkedin_profile]')
			profile.githuburl = request.POST.get('user[github_profile]')
			profile.example = request.POST.get('user[homepage]')

			#password2 = request.POST.get('user[password_confirmation]')


			profile_form.save(commit=True)
			user_form.save(commit=True)
			return redirect('fosssite:profileuser')
		else:
			print "*"*20
			print 'New'
			print "*"*20
			print profile_form.errors
			print "*"*20
			print user_form.errors
	else:
		profile_form = UserProfileForm()
		user_form = UserEditForm(instance=request.user)
	return  render(request,'fosssite/tempedit.html',{'profile_form':profile_form, 'user_form':user_form})
"""
def invalid_login(request):
	return render_to_response('fosssite/invalid_login.html')

def view_profile(request):
    url = request.user.profile.url
"""
