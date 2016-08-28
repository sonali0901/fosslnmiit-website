from django.contrib.auth.models import User
from django import forms
from .models import UserProfile, Contributions, Speakers

LNMIIT_DOMAIN="@lnmiit.ac.in"


class UserForm(forms.ModelForm):
	password=forms.CharField(widget=forms.PasswordInput)

	def clean_email(self):
		data = self.cleaned_data['email']
		if LNMIIT_DOMAIN not in data:
			raise forms.ValidationError("Must be a college domain")
		return data

	class Meta:
		model=User
		fields=['username','email','first_name','last_name','password']

class UserProfileForm(forms.ModelForm):


	class Meta:
		model= UserProfile
		exclude= ('profileuser',)



class UserEditForm(forms.ModelForm):

	class Meta:
		model = User
		fields = ['email','first_name','last_name']

class ContributionsForm(forms.ModelForm):
	ticket_id = forms.IntegerField(required=False)
	contribution_link = forms.URLField(required=False)
	organization = forms.CharField(max_length=200,required=False)

	class Meta:
		model = Contributions
		exclude = ('contributionsuser',)

class SpeakersForm(forms.ModelForm):

	class Meta:
		model = Speakers
		exclude =('speakersuser',)
