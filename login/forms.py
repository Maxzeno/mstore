from django.shortcuts import redirect
from django import forms
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from core.models import User


class SigninForm(forms.Form):
	email = forms.EmailField(required=False, max_length=100, widget=forms.TextInput(attrs={
		'placeholder':'you@gmail.com',
	}))

	password = forms.CharField(required=False, max_length=32, widget=forms.PasswordInput(attrs={
		'placeholder':'your password',
	}))

	def clean(self):
		email = self.cleaned_data.get('email')
		password = self.cleaned_data.get('password')
		user = User.objects.filter(email=email).first()

		if user:
			is_auth = user.check_password(password)
			# is_auth2 = authenticate(username=user.username, password=password)
			if is_auth:
				return email
			raise forms.ValidationError('Invalid Login')

		raise forms.ValidationError('Invalid Login')


class SignupForm(forms.Form):
	name = forms.CharField(required=False, label='', max_length=100,  widget=forms.TextInput(attrs={
		'placeholder':'Name', 'class': 'form-control'
		}))
	email = forms.EmailField(required=True, label='', max_length=100,  widget=forms.EmailInput(attrs={
		'placeholder':'Email', 'class': 'form-control', 'id': 'inputEmail4'
		}))
	whatsapp_number = forms.CharField(required=True, label='', max_length=30,  widget=forms.TextInput(attrs={
		'placeholder':'Whatsapp', 'class': 'form-control'
		}))
	password = forms.CharField(required=True, label='', max_length=128, widget=forms.PasswordInput(attrs={
		'placeholder':'Enter Password', 'class': 'form-control', 'id': 'fakePassword'
		}))

	def clean_name(self):
		name = self.cleaned_data.get('name')
		found_name = User.objects.filter(name=name.lower()).first()
		if found_name:
			raise forms.ValidationError('Name Exists')
		return name.lower()

	def clean_email(self):
		email = self.cleaned_data.get('email')
		found_email = User.objects.filter(email=email.lower()).first()
		if found_email:
			raise forms.ValidationError('Email Exists')
		return email.lower()

	def clean_whatsapp_number(self):
		whatsapp_number = self.cleaned_data.get('whatsapp_number')
		found_whatsapp_number = User.objects.filter(whatsapp_number=whatsapp_number.lower()).first()
		if found_whatsapp_number:
			raise forms.ValidationError('Whatsapp Number Exists')
		return whatsapp_number.lower()


	def clean_password(self):
		password = self.cleaned_data.get('password')
		if len(password) < 8 or len(password) > 128:
			if len(password) < 8:
				raise forms.ValidationError('Password should be greater than 7 characters')
			raise forms.ValidationError('Password should be less than 129 characters')

		elif password.isnumeric() or password.isalpha():
			raise forms.ValidationError('Password should contain alphabets and numbers')

		return password
            

class ForgotPasswordForm(forms.Form):
	email = forms.EmailField(required=False, max_length=100, widget=forms.TextInput(attrs={
		'placeholder':'you@gmail.com',
		}))


class ResetPasswordForm(forms.Form):
	password = forms.CharField(label='Password', required=False, max_length=100, widget=forms.PasswordInput(attrs={
		'placeholder':'new password',
		}))

	confirm_password = forms.CharField(label='Confirm', required=False, max_length=100, widget=forms.PasswordInput(attrs={
		'placeholder':'confirm password',
		}))

	def clean_password(self):
		password = self.cleaned_data.get('password')

		if len(password) < 8 or len(password) > 128:
			if len(password) < 8:
				raise forms.ValidationError('Password should be greater than 7 characters')
			raise forms.ValidationError('Password should be less than 129 characters')

		elif password.isnumeric() or password.isalpha():
			raise forms.ValidationError('Password should contain alphabets and numbers')

		return password

	def clean_confirm_password(self):
		password = self.cleaned_data.get('password')
		confirm_password = self.cleaned_data.get('confirm_password')

		if password and password != confirm_password:
			raise forms.ValidationError('The Two Passwords Don\'t match')

		return confirm_password
            




