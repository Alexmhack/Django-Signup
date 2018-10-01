from django.contrib import admin

from .models import Profile

@admin.register(Profile)
class ProfileModelAdmin(admin.ModelAdmin):
	list_display = ('user', 'location')
	list_search_fields = ('user', 'location')
