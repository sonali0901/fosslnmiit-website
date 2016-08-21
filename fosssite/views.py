from django.views.generic import View
from django.utils import timezone
from django.shortcuts import render, get_object_or_404,render_to_response,redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import UserForm, UserProfileForm, UserEditForm
from .models import UserProfile, User




from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template import loader
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from foss.settings import DEFAULT_FROM_EMAIL
from django.views.generic import *
#from .forms import PasswordResetRequestForm, SetPasswordForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models.query_utils import Q


def home(request):
	return render(request, 'fosssite/home.html')

def login_user(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(username=username,password=password)
		if user is not None:
			auth.login(request, user)
			return redirect('fosssite:home')
		else:
			return render(request, 'fosssite/login.html', {'error_message': 'Invalid login'})
	return render(request,'fosssite/login.html')


def UserFormView(request):
	form=UserForm(request.POST or None)
	profile_form = UserProfileForm()
	if form.is_valid():
		# not saving to database only creating object
		user=form.save(commit=False)
		profile = profile_form.save(commit=False)
		#normalized data
		user.first_name = form.data['fname']
		user.last_name = form.data['lname']
		username=form.cleaned_data['username']
		password=form.cleaned_data['password']
		email = form.cleaned_data['email']
		try:
			useremail = User.objects.get(email=email)
		except User.DoesNotExist:
			useremail = None
		if useremail is not None:
			return render(request,'fosssite/signup.html',{'msg':'Email Already Exists!'})
		#not as plain data
		user.set_password(password)
		user.save() #saved to database
		user = auth.authenticate(username=username,password=password)
		if user is not None:
			auth.login(request, user)
			profile.profileuser = request.user
			profile.save()
			return redirect('fosssite:home')
	return render(request,'fosssite/signup.html',{'form':form})

@login_required
def profileuser(request, name):
	userprofile = get_object_or_404(UserProfile,profileuser=request.user)
	return render(request,'fosssite/profileuser.html',{'user':request.user,'userprofile':userprofile})

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
				message = "An email has been sent to " + data +". Please check your inbox to continue reseting password."
				return render(request, 'fosssite/login.html',{'message':message})
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
				messages.success(request,"The reset password link is no longer valid.")
				return redirect('fosssite:forgot_password')
		else:
			return render(request, 'fosssite/confirm_password.html',{})
	else:
		messages.success(request,"The reset password link is no longer valid.")
		return redirect('fosssite:forgot_password')

"""
class ResetPasswordRequestView(FormView):
    template_name = "account/test_template.html"    #code for template is given below the view's code
    success_url = '/login'
    form_class = PasswordResetRequestForm

    @staticmethod
    def validate_email_address(email):
        try:
            validate_email(email)
            return True
        except ValidationError:
            return False

    def post(self, request, *args, **kwargs):

        form = self.form_class(request.POST)

        if form.is_valid():
            data= form.cleaned_data["email_or_username"]

        if self.validate_email_address(data) is True:                 #uses the method written above
            associated_users= User.objects.filter(Q(email=data)|Q(username=data))
            if associated_users.exists():
                for user in associated_users:
                        c = {
                            'email': user.email,
                            'domain': request.META['HTTP_HOST'],
                            'site_name': 'FossLnmiit',
                            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                            'user': user,
                            'token': default_token_generator.make_token(user),
                            'protocol': 'http',
                            }
                        subject_template_name='registration/password_reset_subject.txt'
                        # copied from django/contrib/admin/templates/registration/password_reset_subject.txt to templates directory
                        email_template_name='registration/password_reset_email.html'
                        # copied from django/contrib/admin/templates/registration/password_reset_email.html to templates directory
                        subject = loader.render_to_string(subject_template_name, c)
                        # Email subject *must not* contain newlines
                        subject = ''.join(subject.splitlines())
                        email = loader.render_to_string(email_template_name, c)
                        send_mail(subject, email, DEFAULT_FROM_EMAIL , [user.email], fail_silently=False)
                result = self.form_valid(form)
                messages.success(request, 'An email has been sent to ' + data +". Please check its inbox to continue reseting password.")
                return result
            result = self.form_invalid(form)
            messages.error(request, 'No user is associated with this email address')
            return result
        else:
            associated_users= User.objects.filter(username=data)
            if associated_users.exists():
                for user in associated_users:
                    c = {
                        'email': user.email,
                        'domain': '127.0.0.1:8000/', #or your domain
                        'site_name': 'FossLnmiit',
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'user': user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                        }
                    subject_template_name='registration/password_reset_subject.txt'
                    email_template_name='registration/password_reset_email.html'
                    subject = loader.render_to_string(subject_template_name, c)
                    # Email subject *must not* contain newlines
                    subject = ''.join(subject.splitlines())
                    email = loader.render_to_string(email_template_name, c)
                    send_mail(subject, email, DEFAULT_FROM_EMAIL , [user.email], fail_silently=False)
                result = self.form_valid(form)
                messages.success(request, 'Email has been sent to ' + data +"'s email address. Please check its inbox to continue reseting password.")
                return result
            result = self.form_invalid(form)
            messages.error(request, 'This username does not exist in the system.')
            return result
        messages.error(request, 'Invalid Input')
        return self.form_invalid(form)


class PasswordResetConfirmView(FormView):
    template_name = "account/test_template.html"
    success_url = '/admin/'
    form_class = SetPasswordForm

    def post(self, request, uidb64=None, token=None, *arg, **kwargs):

        View that checks the hash in a password reset link and presents a
        form for entering a new password.

        UserModel = get_user_model()
        form = self.form_class(request.POST)
        assert uidb64 is not None and token is not None  # checked by URLconf
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = UserModel._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            if form.is_valid():
                new_password= form.cleaned_data['new_password2']
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Password has been reset.')
                return self.form_valid(form)
            else:
                messages.error(request, 'Password reset has not been unsuccessful.')
                return self.form_invalid(form)
        else:
            messages.error(request,'The reset password link is no longer valid.')
            return self.form_invalid(form)
"""
