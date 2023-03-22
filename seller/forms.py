from django import forms
from django.contrib import messages
from ckeditor.widgets import CKEditorWidget
from core.models import SubCategory


class ProductForm(forms.Form):
	name = forms.CharField(required=True, label='', max_length=100,  widget=forms.TextInput(attrs={
		'placeholder':'Name', 'class': 'form-control'
	}))

	state = forms.CharField(required=False, label='', max_length=100,  widget=forms.TextInput(attrs={
		'placeholder':'State', 'class': 'form-control'
	}))

	price = forms.CharField(required=True, label='', max_length=100,  widget=forms.NumberInput(attrs={
		'placeholder':'Price', 'class': 'form-control'
	}))

	MY_CHOICES = [ [i.id, i.name] for i in SubCategory.objects.all() ]

	sub_category = forms.ChoiceField(required=True, choices=[['', 'Select an option']]+MY_CHOICES, initial='', widget=forms.Select(attrs={
		'placeholder':'Price', 'class': 'form-select'
	}))

	image = forms.ImageField(required=False, label='', widget=forms.FileInput(attrs={
	'class': 'form-control'
	}))

	description = forms.CharField(required=False, label='', widget=CKEditorWidget(attrs={
		'placeholder':'Description', 'class': 'form-control'
	}))

	def clean_price(self):
		price = self.cleaned_data.get('price')
		if not price:
			raise forms.ValidationError('Provide price')
		elif float(price) <= 0:
			raise forms.ValidationError('Price should be above zero')
		return price

	def clean_sub_category(self):
		sub_category = self.cleaned_data.get('sub_category')
		if not sub_category:
			raise forms.ValidationError('Select sub category')
		return sub_category

	def clean_name(self):
		name = self.cleaned_data.get('name')
		if not name:
			raise forms.ValidationError('Name is required')
		return name


