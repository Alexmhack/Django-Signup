# Django-Signup
Creating a simple sign up view and then moving onto more advanced sign up view with profile model and confirmation mail

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
