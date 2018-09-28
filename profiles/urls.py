from django.urls import path

from .views import signup, ProfileUpdateView

urlpatterns = [
	path('', signup, name='profile-signup'),
	path('<int:pk>/edit/', ProfileUpdateView.as_view(), name='profile-edit'),
]
