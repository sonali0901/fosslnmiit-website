from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import UserForm, UserProfileForm, UserEditForm, ContributionsForm, SpeakersForm
from .models import UserProfile, User, Contributions, Speakers
from django.forms import formset_factory
from django.db import IntegrityError, transaction
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template import loader
from django.core.mail import send_mail
from foss.settings import DEFAULT_FROM_EMAIL
from django.contrib import messages
from django.contrib.auth.models import User


def home(request):
	return render(request, 'fosssite/home.html')

def login_user(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		try:
			user = User.objects.get(username=username)
		except User.DoesNotExist:
			user = None

		try:
			if user.is_active:
				user = authenticate(username=username,password=password)
				if user is not None:
					auth.login(request, user)
					return redirect('fosssite:home')
				else:
					return render(request, 'fosssite/login.html', {'error_message': 'Invalid login'})
			else:
				return redirect('fosssite:signup_email')
		except:
			return render(request, 'fosssite/login.html', {'error_message': 'Invalid login'})
	return render(request,'fosssite/login.html')

def signup_email(request):
	if request.method == 'POST':
		if not request.POST.get('signup_email'):
			return render(request, 'fosssite/signup_email.html',{'error':'Please Enter Credentials!'})
		else:
			data = request.POST.get('signup_email')

		try:
			user = User.objects.get(email=data)
		except User.DoesNotExist:
			user = None
		#user= User.objects.filter(email=data)
		if user is not None:
			c = {
				'email': user.email,
				'domain': '127.0.0.1:8000', #or your domain
				'site_name': 'FossLnmiit',
				'uid': urlsafe_base64_encode(force_bytes(user.pk)),
				'user': user,
				'token': default_token_generator.make_token(user),
				'protocol': 'http',
				}
			subject_template_name='signup/email_confirm_subject.txt'
			email_template_name='signup/email_confirm_email.html'
			subject = loader.render_to_string(subject_template_name, c)
			# Email subject *must not* contain newlines
			subject = ''.join(subject.splitlines())
			email = loader.render_to_string(email_template_name, c)
			send_mail(subject, email, DEFAULT_FROM_EMAIL , [user.email], fail_silently=False)
			messages.success(request,"An email has been sent to " + data +". Please check your inbox to signup.")
			return redirect('fosssite:home')
		else:
			error = "No user is associated with this Email Address."
			return render(request,'fosssite/signup_email.html',{'error':error})
	return render(request, 'fosssite/signup_email.html',{})

def confirm_email(request, uidb64=None, token=None):
	assert uidb64 is not None and token is not None  # checked by URLconf
	try:
		uid = urlsafe_base64_decode(uidb64)
		user = User.objects.get(pk=uid)
	except:
		user = None

	if user is not None:
		if default_token_generator.check_token(user, token):
			user.is_active = True
			user.save()
			messages.success(request, "Email Address Verified! Please Login to continue !")
			return redirect('fosssite:home')
		else:
			messages.success(request,"The email verification link is no longer valid. Try again!")
			return redirect('fosssite:signup_email')
	else:
		messages.success(request,"The email verification link is no longer valid. Try again!")
		return redirect('fosssite:signup_email')

def UserFormView(request):
	form=UserForm(request.POST or None)
	profile_form = UserProfileForm()
	contributions_form = ContributionsForm()
	speakers_form = SpeakersForm()
	if form.is_valid():
		# not saving to database only creating object
		user=form.save(commit=False)
		profile = profile_form.save(commit=False)
		contributions = contributions_form.save(commit=False)
		speakers = speakers_form.save(commit=False)
		#normalized data
		user.first_name = form.data['fname']
		user.last_name = form.data['lname']
		username=form.cleaned_data['username']
		password=form.cleaned_data['password']
		email = form.cleaned_data['email']
		try:
			profile.is_public = form.data['is_public']
		except:
			profile.is_public = False

		try:
			useremail = User.objects.get(email=email)
		except User.DoesNotExist:
			useremail = None
		if useremail is not None:
			return render(request,'fosssite/signup.html',{'msg':'Email Already Exists!'})
		#not as plain data
		user.set_password(password)
		user.is_active = False
		user.save() #saved to database
		profile.profileuser = user
		profile.save()
		contributions.contributionsuser = user
		contributions.save()
		speakers.speakersuser = user
		speakers.save()
		c = {
			'email': user.email,
			'domain': '127.0.0.1:8000', #or your domain
			'site_name': 'FossLnmiit',
			'uid': urlsafe_base64_encode(force_bytes(user.pk)),
			'user': user,
			'token': default_token_generator.make_token(user),
			'protocol': 'http',
			}
		subject_template_name='signup/email_confirm_subject.txt'
		email_template_name='signup/email_confirm_email.html'
		subject = loader.render_to_string(subject_template_name, c)
		# Email subject *must not* contain newlines
		subject = ''.join(subject.splitlines())
		email = loader.render_to_string(email_template_name, c)
		send_mail(subject, email, DEFAULT_FROM_EMAIL , [user.email], fail_silently=False)
		messages.success(request,"An email has been sent to " + user.email +". Please check your inbox to signup.")
		return redirect('fosssite:home')
	return render(request,'fosssite/signup.html',{'form':form})


def profileuser(request, name):
	try:
		request.user
		userprofile = get_object_or_404(UserProfile,profileuser=request.user)
		return render(request,'fosssite/profileuser.html',{'user':request.user,'userprofile':userprofile,'puser':None})
	except:
		public_user = User.objects.filter(username=name).first()
		if public_user:
			public_userprofile = get_object_or_404(UserProfile,profileuser=public_user)
			if public_userprofile.is_public:
				return render(request,'fosssite/profileuser.html',{'puser':public_user,'userprofile':public_userprofile,'user':public_user})
			return redirect('fosssite:login_user')
		return redirect('fosssite:login_user')

@login_required
def logout(request):
	auth.logout(request)
	return HttpResponseRedirect('/')

@login_required
def edit_user_profile(request, name):
	puser = get_object_or_404(UserProfile, profileuser= request.user)
	if request.method == 'POST':

		profile_form = UserProfileForm(data=request.POST, instance=puser)
		user_form = UserEditForm(data=request.POST, instance=request.user)
		if user_form.is_valid() and profile_form.is_valid():

			profile = profile_form.save(commit=False)
			profile.profileuser = request.user
			if 'avatar' in request.FILES:
				profile.avatar = request.FILES['avatar']
				if profile.avatar.size > 1048576:
					errors= 'Max File Size is 1 MB'
					return render(request,'fosssite/edituser.html',{'profile_form':profile_form,'user_form':user_form,'errors':errors})
			profile_form.save()
			user_form.save()
			return redirect('fosssite:profileuser',name=request.user)
	else:
		profile_form = UserProfileForm(instance=puser)
		user_form = UserEditForm(instance=request.user)
	return  render(request,'fosssite/edituser.html',{'profile_form':profile_form, 'user_form':user_form})

@login_required
def changepassword(request, name):
	if request.method=='POST':
		user = User.objects.get(username=request.user)
		current_password = request.POST.get('current_password')
		if user.check_password(current_password):
			password1 = request.POST.get('password1')
			password2 = request.POST.get('password2')
			if password1 == password2 and len(password1) !=0:
				user.set_password(password1)
				user.save()
				user = auth.authenticate(username=user.username,password=password1)
				if user is not None:
					auth.login(request, user)
					return redirect('fosssite:profileuser', name=request.user)
			else:
				error = 'New Password Must Match or valid!'
				return render(request, 'fosssite/changepassword.html',{'error':error})
		else:
			error = 'Current Password not Matched!'
			return render(request,'fosssite/changepassword.html',{'error':error})
	return render(request,'fosssite/changepassword.html')


@login_required
def edit_contributions(request, name):
	ContributionsFormSet = formset_factory(ContributionsForm)
	user = request.user

	user_links = Contributions.objects.filter(contributionsuser=user).order_by('organization')
	link_data = [{'ticket_id':l.ticket_id,'contribution_link':l.contribution_link,'organization':l.organization} 	for  l in user_links]

	if request.method == 'POST':
		contributions_formset = ContributionsFormSet(request.POST)
		if contributions_formset.is_valid():
			new_data =[]

			for contributions_form in contributions_formset:
				contributionsuser = user
				ticket_id = contributions_form.cleaned_data.get('ticket_id')
				contribution_link = contributions_form.cleaned_data.get('contribution_link')
				organization = contributions_form.cleaned_data.get('organization')

				if ticket_id and contribution_link and organization:
					new_data.append(Contributions(contributionsuser=contributionsuser, ticket_id=ticket_id,contribution_link=contribution_link,organization=organization))
				else:
					contributions_formset = ContributionsFormSet(initial=link_data)
					context = {
						'contributions_formset':contributions_formset,
						'error':"Fields can't be empty!"
					}
					return render(request, 'fosssite/edit_contributions.html',context)
			try:
				with transaction.atomic():
					Contributions.objects.filter(contributionsuser=user).delete()
					Contributions.objects.bulk_create(new_data)
					messages.success(request, 'You have updated your profile.')
					return redirect('fosssite:home')
			except:
				messages.error(request, 'There was an error saving your profile.')
				return redirect('fosssite:home')

	else:
		contributions_formset = ContributionsFormSet(initial=link_data)
	context = {
		'contributions_formset':contributions_formset,
	}

	return render(request, 'fosssite/edit_contributions.html',context)

@login_required
def edit_speakers(request, name):
	SpeakersFormSet = formset_factory(SpeakersForm)
	user = request.user

	user_links = Speakers.objects.filter(speakersuser=user).order_by('event_name')
	link_data = [{'event_name':l.event_name,'event_link':l.event_link} 	for  l in user_links]

	if request.method == 'POST':
		speakers_formset = SpeakersFormSet(request.POST)
		if speakers_formset.is_valid():
			new_data =[]
			for speakers_form in speakers_formset:
				speakersuser = user
				event_name = speakers_form.cleaned_data.get('event_name')
				event_link = speakers_form.cleaned_data.get('event_link')

				if event_name and event_name:
					new_data.append(Speakers(speakersuser=speakersuser, event_name=event_name,event_link=event_link))
				else:
					speakers_formset = SpeakersFormSet(initial=link_data)
					context = {
						'speakers_formset':speakers_formset,
						'error':"Fields can't be empty!"
					}
					return render(request, 'fosssite/edit_speakers.html',context)

			try:
				with transaction.atomic():
					Speakers.objects.filter(speakersuser=user).delete()
					Speakers.objects.bulk_create(new_data)
					messages.success(request, 'You have updated your profile.')
					return redirect('fosssite:home')
			except:
				messages.error(request, 'There was an error saving your profile.')
				return redirect('fosssite:home')

	else:
		speakers_formset = SpeakersFormSet(initial=link_data)
		context = {'speakers_formset':speakers_formset}
	return render(request, 'fosssite/edit_speakers.html',context)


def events(request):
	if request.user.is_authenticated():
		return render(request,'fosssite/working.html',{})
	return render(request, 'fosssite/events.html')


def contributions(request):
	if request.user.is_authenticated():
		return render(request,'fosssite/working.html',{})
	return render(request, 'fosssite/contributions.html')


def blog(request):
	if request.user.is_authenticated():
		return render(request,'fosssite/working.html',{})
	return render(request, 'fosssite/blog.html')

def forgot_password(request):
	if request.method == 'POST':
		if not request.POST.get('email'):
			return render(request, 'fosssite/forgotpassword.html',{'error':'Please Enter Credentials!'})
		else:
			data = request.POST.get('email')
			try:
				user = User.objects.get(email=data)
			except User.DoesNotExist:
				user = None
			#user= User.objects.filter(email=data)
			if user is not None:
				c = {
					'email': user.email,
					'domain': '127.0.0.1:8000', #or your domain
					'site_name': 'FossLnmiit',
					'uid': urlsafe_base64_encode(force_bytes(user.pk)),
					'user': user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
				subject_template_name='email/password_reset_subject.txt'
				email_template_name='email/password_reset_email.html'
				subject = loader.render_to_string(subject_template_name, c)
				# Email subject *must not* contain newlines
				subject = ''.join(subject.splitlines())
				email = loader.render_to_string(email_template_name, c)
				send_mail(subject, email, DEFAULT_FROM_EMAIL , [user.email], fail_silently=False)
				messages.success(request,"An email has been sent to " + data +". Please check your inbox to continue reseting password.")
				return redirect('fosssite:home')
			else:
				error = "No user is associated with this Email Address."
				return render(request,'fosssite/forgotpassword.html',{'error':error})
	return render(request,'fosssite/forgotpassword.html',{})

def confirm_password(request, uidb64=None, token=None):
	assert uidb64 is not None and token is not None  # checked by URLconf
	try:
		uid = urlsafe_base64_decode(uidb64)
		user = User.objects.get(pk=uid)
	except:
		user = None

	if user is not None:
		if request.method == 'POST':
			if default_token_generator.check_token(user, token):
				password1 = request.POST.get('password1')
				password2 = request.POST.get('password2')
				if password1 == password2 and len(password1) !=0:
					user.set_password(password1)
					user.save()
					messages.success(request,'Password Changed!')
					return redirect('fosssite:login_user')
				else:
					messages.success(request,'Both Passwords Must Match. Please try again!')
					return redirect('fosssite:confirm_password',uidb64=uidb64, token=token)
			else:
				messages.success(request,"The reset password link is no longer valid. Try again!")
				return redirect('fosssite:forgot_password')
		else:
			return render(request, 'fosssite/confirm_password.html',{})
	else:
		messages.success(request,"The reset password link is no longer valid. Try again!")
		return redirect('fosssite:forgot_password')
