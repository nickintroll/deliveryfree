from django import forms 
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import Profile


class LoginForm(forms.Form):
	username = forms.CharField(widget=forms.TextInput(
		attrs={'placeholder': 'username'}
		), label='')
	password = forms.CharField(widget=forms.PasswordInput(
		attrs={'placeholder': 'password'}
		), label='')


class RegisterForm(forms.ModelForm):
	password1 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder':'Passowrd'}))
	password2 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder':'Repeat passowrd'}))


	class Meta:
		model = User
		fields = ('username', 'email')
		widgets = {
			'username': forms.TextInput(attrs={'placeholder': 'Username'}),
			'email': forms.TextInput(attrs={'placeholder': 'Email'})
		}

	def clean_password(self):
		cd = self.cleaned_data
		if cd['password1'] != cd['password2']:
			raise ValidationError('Password do\'t match.')
		else:
			return cd['password2']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields["username"].label = ''
		self.fields["username"].help_text = ''
		self.fields["email"].label = ''
		self.fields["email"].help_text = ''


class UpdateProfileForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ('description', 'birth_date', 'education', 'picture')


class EmployeeSearchForm(forms.Form):
	search = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'search'}), required=False)
	age_from = forms.IntegerField(label='', widget=forms.NumberInput(attrs={'placeholder': 'age from'}), required=False)
	age_to = forms.IntegerField(label='', widget=forms.NumberInput(attrs={'placeholder': 'age to'}), required=False)
	
