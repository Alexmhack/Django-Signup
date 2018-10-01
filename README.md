# Django-Signup
Creating a simple sign up view and then moving onto more advanced sign up view with profile model and confirmation mail

**I have also added a location field in custom profile model and stored the 
actual location (city, country code) of user using API, a little javascript and 
python without letting user know about it. For a tutorial on using that API checkout my [repo](https://github.com/Alexmhack/django_weather_app)**

In this tutorial we will 

1. Create basic sign up view
2. Create sign up form with extra fields
3. Create profile model for users
4. Create sign up view with confirmation email

# Finished View
After completing the project and adding some styling from [mdbootstrap](http://mdbootstrap.com/) my project looks like

Home Page is simply showing a navbar with working links

![Home Page](https://github.com/Alexmhack/Django-Signup/blob/master/readme_images/home.PNG)

Login page looks like 

![signin Page](https://github.com/Alexmhack/Django-Signup/blob/master/readme_images/signin.PNG)

Sign Up page

![signup Page](https://github.com/Alexmhack/Django-Signup/blob/master/readme_images/signup.PNG)

And finally dashboard page with the user name displayed...

![dashboard Page](https://github.com/Alexmhack/Django-Signup/blob/master/readme_images/dashboard.PNG)

**You can reuse the code from my repo and include it in your django project. Put a star if you liked my work.**

# Django Project Setup

```
pip install -r requirements.txt
```

1. ```django-admin startproject website .```
2. ```python manage.py migrate```
3. ```python manage.py createsuperuser```
4. ```python manage.py runserver```
5. In project ```settings.py``` file import [decouple](https://pypi.org/project/python-decouple/)

	```
	from decouple import config
	SECRET_KEY = config("PROJECT_KEY")
	```

	And create ```.env``` file like so

	```
	PROJECT_KEY=93%@nka8)+fv-*ai-st1d*h)w2j2-y^)(jfiv9bogcy0u241u7
	```

We will start with the basic sign up features that django provides by default

# Basic Sign Up
Simplest way to implement a **Sign Up** view is using ```UserCreationForm```. 
This form is for those django apps which use the default user model that only 
contains a **username** and **password** for user sign ups.

To implement that view we need

**urls.py**
```
...
from .views import signup_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', signup_view, name='sign-up'),
]
```

In ```urls.py``` we simply import the ```signup_view``` that we haven't yet added 
to ```views.py``` and create a url for that view.

Now create ```views.py``` file in the **website** folder and put this code inside 
it.

```
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm

def signup(request):
	if request.method == "POST":
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password1')
			user = authenticate(username=username, password=password)
			login(request, user)
			return redirect('home')
		else:
			form = UserCreationForm()

		return render(request, 'signup.html', {'form': form})
```

This is most basic signup view that django has. All of the new user creation 
process is done using django. We use the default ```UserCreationForm``` form to 
display the signup form. We authenticate the new user using the username and 
password that we get from the post request from the **form**. We then login the 
user and redirect it to ```home``` view. If the request method is not ```POST``` 
we simply show the empty form in ```templates/signup.html``` file.

Create a **templates** folder in root path (where ```manage.py``` file lies). In
that folder create ```signup.html``` file.

**signup.html**
```
{% extends 'base.html' %}

{% block content %}
  <h2>Sign up</h2>
  <form method="post">
    {% csrf_token %}
    {% for field in form %}
      <p>
        {{ field.label_tag }}<br>
        {{ field }}
        {% if field.help_text %}
          <small style="color: grey">{{ field.help_text }}</small>
        {% endif %}
        {% for error in field.errors %}
          <p style="color: red">{{ error }}</p>
        {% endfor %}
      </p>
    {% endfor %}
    <button type="submit">Sign up</button>
  </form>
{% endblock %}
```

This is a little different way of rendering form. There are more ways like

```
{{ form.as_p }} 
{{ form.as_table }}
{{ form.as_ul }} 
```

# Sign Up Form With Extra Fields
So far we have been using the default fields that ```UserCreationForm``` provides
us. But what if we wanted the email address of the new user which is the 
important part aside from the username and password. 

For that we can inherit a new form class from ```UserCreationForm```. Create a 
new file named ```forms.py``` in the **website** folder. All of this should go 
in a separate app so you can start another app. Let's just do that as our project
is increasing in size.

```
python manage.py startapp users
```

Include app in project **settings**

```
...
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users',
]
```

Move the file ```website/views.py``` to ```users``` folder and replace it.
These are some of the changes which you would have to do a lot of times if you 
are working on a large project in any language.

Since we moved the ```views.py``` file, all our imports in ```urls.py``` will 
give errors. Let's also create a ```urls.py``` file in ```users``` folder.

From the **website/urls.py** file change this piece of code into

```
from .views import signup_view, dashboard_view, home_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', signup_view, name='sign-up'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('', home_view, name='home'),
]
```

replace with below code

```
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls', namespace='users')),
]
```

Now we will create a custom user registration form so create a new file ```forms.py``` in **users** folder.

```
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
	first_name = forms.CharField(
		max_length=10,
		min_length=4,
		required=True,
		widget=forms.TextInput(
				attrs={
					"placeholder": "First Name",
					"class": "form-control"
				}
			)
		)
	last_name = forms.CharField(
		max_length=30,
		required=True,
		widget=forms.TextInput(
				attrs={
					"placeholder": "Last Name",
					"class": "form-control"
				}
			)
		)
	email = forms.EmailField(
		max_length=254,
		widget=forms.EmailInput(
			attrs={
				"placeholder": "Email",
				"class": "form-control"
			}
		)
	)

	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)
```

You can do the same with ```password``` fields by using ```PasswordInput()```

```
...
	password1 = forms.CharField(
		label='',
		max_length=30,
		min_length=8,
		required=True,
		widget=forms.PasswordInput(
			attrs={
				"placeholder": "Password",
				"class": "form-control"
			}
		)
	)

	password2 = forms.CharField(
		label='',
		max_length=30,
		min_length=8,
		required=True,
		widget=forms.PasswordInput(
			attrs={
				"placeholder": "Confirm Password",
				"class": "form-control"
			}
		)
	)
```

This would give the forms a nice look as well as placeholders and the rest of 
the django password validation remains intact and active.

# Sign Up With Profile Model
So far we have been using the ```User``` model from 
```django.contrib.auth.models``` that meets almost all needs but **Django** docs
itself recommends using a custom model for users instead of the ```User``` so in
this section we will be making our own custom model for users and name it 
```Profile```

For this part we will start another app name ```profiles```

```
python manage.py startapp profiles
```

Add profiles app in **settings**

Inside ```profiles/models.py``` add 

```
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
```

In this particular case, the profile is created using a Signal. It’s not 
mandatory, but usually it is a good way to implement it.

```
class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	bio = models.CharField(max_length=50, blank=True)
	location = models.CharField(max_length=30, blank=True)


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
```

This is our custom model, ofcourse you can go far more further adding in birth
date, and profile image and lots more stuff, but for simplicity we are just using
three fields.

Now we need to create a form so ```forms.py``` file should have

```
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    birth_date = forms.DateField(help_text='Required. Format: YYYY-MM-DD')

    class Meta:
        model = User
        fields = ('username', 'birth_date', 'password1', 'password2', )
```

You can add in attributes in the fields again like we did earlier.

There are a few changes that ```views.py``` file should have

```
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from mysite.core.forms import SignUpForm

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.profile.birth_date = form.cleaned_data.get('birth_date')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})
```

Because of the Signal handling the Profile creation, we have a synchronism issue 
here. It is easily solved by calling the user.refresh_from_db() method. This 
will cause a hard refresh from the database, which will retrieve the profile 
instance.

If you don’t call user.refresh_from_db(), when you try to access the 
user.profile, it will return None.

After refreshing it user model, set the cleaned data to the fields that matter, 
and save the user model. The user save will trigger the profile save as well, 
that’s why you don’t need to call user.profile.save(), instead you call just 
user.save().

You can display the user details using 

```
	<h1 class="mt-5 text-center">Welcome {{ request.user }}</h1>
	<p class="text-left mt-5">Bio: {{ user.profile.bio }}</p>
	<p class="text-left">Location: {{ user.profile.location }}</p>
	<p class="text-left">Joined: {{ user.profile.timestamp }}</p>
```

**For customizing the forms you can use [django-widget-tweaks](https://pypi.org/project/django-widget-tweaks/)**

# Signup With Confirmation Email
Django provides built-in system for sending emails. But first of test purposes 
we will be using **Console Backend** for emails. 

Add this settings in ```settings.py``` file

```
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

Now for checking if a user is authenticated we will create a field in the profile 
model to determine if the user is confirmed or not.

**profiles/models.py**
```
class Profile(models.Model):
	...
	email_confirmed = models.BooleanField(default=False)
```

And for creating a one time link using django we will create a new file ```tokens.py```

```
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
	def _make_hash_value(self, user, timestamp):
		return (
			six.text_type(user.pk) + six.text_type(timestamp) +
			six.text_type(user.profile.email_confirmed)
		)


account_activation_token = AccountActivationTokenGenerator()
```

We use the ```pk``` from the user ```timestamp``` and the ```email_confirmed``` field
to create a token. We basically extended the PasswordResetTokenGenerator to create a 
unique token generator to confirm email addresses. This make use of your project’s 
SECRET_KEY, so it is a pretty safe and reliable method.

Now we need to define views for account activation as well as account activation sent 
view

```
def account_activation_sent_view(request):
    return render(request, 'registration/account_activation_sent.html')


def account_activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        print(uid)
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
        print(e)
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('users:dashboard')
    else:
        return render(request, 'registration/account_activation_invalid.html')
```

```account_activation_sent_view``` is justfor redirecting users if their account activation url is wrong. The template **registration/account_activation_sent.html**
will be

```
{% extends "base.html" %}

{% block title %}
	{{ block.super }} - Check Your Email Account
{% endblock %}

{% block content %}

	<h3 class="text-center">Check your email account for verifying your django account.</h3>
	
{% endblock %}
```

```account_activate``` function simply fetches the ```uidb64``` and ```token```
from the url and uses the **.check_token** function from ```AccountActivationTokenGenerator``` class which takes the user and token.

You can remove the print statements from the code, I use them for testing purposes 
while writing my code.

**profiles/views.py**
```
User = get_user_model()

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            user = form.save()
            current_site = get_current_site(request)
            subject = "Activate your Django Serives Account"
            message = render_to_string('registration/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user)
            })
            user.email_user(subject, message)
            return redirect('profiles:account-activation-sent')
    else:
        form = SignUpForm()
    return render(request, 'app/signup.html', {
        'form': form,
        'profile': True
    })
```

This is the code for sending email to the user email, notice we have removed 
```user.refresh_from_db()``` since we are using ```form.save(commit=False)```
so you can use ```user.refresh_from_db()``` after saving the form

```
	...
		if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            user = form.save()
            user.refresh_from_db()
            # your code here
           	user.save()		# call save again
           	...
```

This is it. We can extend our model by using the ```smtp``` as email backend that 
will actually send email to the email provided by the user but it requires some more
settings to be defined in the **settings.py** file. For more details visit [docs](https://docs.djangoproject.com/en/2.1/topics/email/)
