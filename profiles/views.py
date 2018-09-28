from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.views.generic import UpdateView
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import SignUpForm
from .models import Profile

def signup(request):
    if request.user.is_authenticated:
        return redirect('users:dashboard')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('users:dashboard')
    else:
        form = SignUpForm()
    return render(request, 'app/signup.html', {
        'form': form,
        'profile': True
    })


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    template_name = "app/profile_edit.html"
    fields = ('bio',)
