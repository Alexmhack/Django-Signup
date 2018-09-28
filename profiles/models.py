from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .utils import get_location_from_ip

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	bio = models.CharField(max_length=50, blank=True)
	location = models.CharField(max_length=30)

	timestamp = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)
		user = Profile.objects.get(user=instance)
		ip_address = user.location
		location = get_location_from_ip(ip_address)
		print(location)
		print(ip_address)
		user.location = location
		user.save()
	instance.profile.save()
