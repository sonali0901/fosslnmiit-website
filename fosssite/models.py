from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

class UserProfile(models.Model):
	profileuser = models.OneToOneField(User)
	handle = models.CharField(max_length=128, blank=True,default='')
	#avatar = models.FileField(default='')
	about_me = models.TextField(max_length=300,blank=True,default='')
	twitterurl = models.URLField(blank=True,default='')
	facebookurl = models.URLField(blank=True,default='')
	lnkdnurl = models.URLField(blank=True,default='')
	githuburl = models.URLField(blank=True,default='')
	example = models.URLField(blank=True,default='')
