from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
	first_name = forms.CharField(
		label='',
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
		fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )
