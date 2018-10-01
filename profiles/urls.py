from django.urls import path, re_path

from .views import (
	signup, ProfileUpdateView, account_activation_sent_view, activate
)

urlpatterns = [
	path('', signup, name='profile-signup'),
	path('<int:pk>/edit/', ProfileUpdateView.as_view(), name='profile-edit'),
]

urlpatterns += [
	path('account-activation-sent/', account_activation_sent_view, name='account-activation-sent'),
	re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
		activate, name='activate'),
]
