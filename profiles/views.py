from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.views.generic import UpdateView
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text

from .forms import SignUpForm
from .models import Profile
from .utils import get_location_from_ip
from .tokens import account_activation_token

def signup(request):
    if request.user.is_authenticated:
        return redirect('users:dashboard')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.refresh_from_db()  # load the profile instance created by the signal
            user.profile.location = form.cleaned_data.get('location')
            ip_address = user.profile.location
            location = get_location_from_ip(ip_address)
            user.profile.location = location
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = "Activate your Django Serives Account"
            message = render_to_string('registration/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user)
            })
            user.email_user(subject, message)
            return redirect('account-activation-sent')
    else:
        form = SignUpForm()
    return render(request, 'app/signup.html', {
        'form': form,
        'profile': True
    })


def account_activation_sent_view():
    return render(request, 'registration/account_activation_sent.html')


def account_activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_encode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('dashboard')


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    template_name = "app/profile_edit.html"
    fields = ('bio',)
