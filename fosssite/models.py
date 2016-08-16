from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

class UserProfile(models.Model):
	user = models.OneToOneField(User)
	handle = models.CharField(max_length=128, blank=True)
	#avatar = models.FileField(default='')
	about_me = models.TextField(blank=True)
	twitterurl = models.URLField(blank=True)
	facebookurl = models.URLField(blank=True)
	lnkdnurl = models.URLField(blank=True)
	githuburl = models.URLField(blank=True)
	example = models.URLField(blank=True)
