from django.shortcuts import render
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect

# Create your views here.

def home(request):
	return render(request, 'fosssite/home.html')
def signup(request):
	return render(request,'fosssite/signup.html')
