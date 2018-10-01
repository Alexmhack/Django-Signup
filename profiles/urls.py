from django.urls import path, re_path

from .views import (
	signup, ProfileUpdateView, account_activation_sent_view, account_activate
)

app_name = 'profiles'

urlpatterns = [
	path('', signup, name='profile-signup'),
	path('<int:pk>/edit/', ProfileUpdateView.as_view(), name='profile-edit'),
]

urlpatterns += [
	path('account-activation-sent/', account_activation_sent_view, name='account-activation-sent'),
	path('activate/<uidb64>/<token>/',
		account_activate, name='activate'),
]
