from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import SignUpForm

def signup_view(request):
	if request.user.is_authenticated:
		return redirect('users:dashboard')
	if request.method == "POST":
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password1')
			user = authenticate(username=username, password=password)
			login(request, user)
			return redirect('users:dashboard')
		else:
			messages.error(request, 'Correct the errors below')
	else:
		form = SignUpForm()

	return render(request, 'app/signup.html', {'form': form})


@login_required
def dashboard_view(request):
	return render(request, 'app/dashboard.html')


def home_view(request):
	return render(request, 'app/home.html')
