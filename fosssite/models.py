

from django.contrib.auth.models import User
from django.db import models
#from django.utils import timezone
#from django.core.exceptions import ValidationError


class UserProfile(models.Model):
	profileuser = models.OneToOneField(User)
	handle = models.CharField(max_length=128, blank=True)
	avatar = models.ImageField(upload_to='profile_images', blank=True)
	about_me = models.TextField(max_length=100,blank=True)
	twitterurl = models.URLField(blank=True)
	facebookurl = models.URLField(blank=True)
	lnkdnurl = models.URLField(blank=True)
	githuburl = models.URLField(blank=True)
	example = models.URLField(blank=True)
	blog_xml = models.URLField(blank=True)
	is_public = models.BooleanField(default=False)

	def __str__(self):
		return self.profileuser.username


class Contributions(models.Model):
	contributionsuser = models.ForeignKey(User)
	ticket_id = models.IntegerField(blank=True, null=True)
	contribution_link = models.URLField(blank=True)
	organization = models.CharField(max_length=200,blank=True)

	def __str__(self):
		return "%s - %s " %(self.contributionsuser.username, self.organization)

class Speakers(models.Model):
	speakersuser = models.ForeignKey(User)
	event_name = models.CharField(max_length=200,blank=True)
	event_link = models.URLField(blank=True)

	def __str__(self):
		return "%s - %s " %(self.speakersuser.username, self.event_name)
