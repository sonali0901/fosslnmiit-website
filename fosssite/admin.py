from django.contrib import admin

# Register your models here.
from fosssite.models import UserProfile, Contributions, Speakers

admin.site.register(UserProfile)
admin.site.register(Contributions)
admin.site.register(Speakers)
