from django.contrib import admin
from django.urls import path

from .views import signup_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', signup_view, name='sign-up'),
]
