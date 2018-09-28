from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', signup_view, name='sign-up'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('', home_view, name='home'),
]
