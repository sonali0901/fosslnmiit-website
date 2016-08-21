"""foss URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static
from fosssite.views import ResetPasswordRequestView, PasswordResetConfirmView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'', include('fosssite.urls')),
    url(r'^accounts/password/reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
  'django.contrib.auth.views.password_reset_confirm',
 {'post_reset_redirect': '/login'}, name='password_reset_confirm'),
    url(r'^account/reset_password', ResetPasswordRequestView.as_view(), name="reset_password"),

]

urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
