from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import User, Order
from .forms import UserDataForm, UserPasswordForm, AddressForm
from main.views import Base
# Create your views here.

def error_404(request, exception):
    return render(request, 'main/404.html', {})


class Orders(LoginRequiredMixin, Base):
	def get_request(self, request):
		orders = Order.objects.filter(buyer=request.user.id)
		return (request, 'core/orders.html', {'orders': orders, 'nav_account': 'green'})


class Address(LoginRequiredMixin, Base):
	def get_request(self, request):
		user = request.user
		address_form = AddressForm({'state': user.state, 'address': user.address})
		return (request, 'core/address.html', {'address_form': address_form, 'nav_account': 'green'})


class UserAddress(LoginRequiredMixin, View):
	def get(self, request):
		return redirect(reverse('core:address'))

	def post(self, request):
		form = AddressForm(request.POST)
		if form.is_valid():
			user = User.objects.get(pk=request.user.id)
			user.state = form.cleaned_data.get('state')
			user.address = form.cleaned_data.get('address')
			user.save()
			messages.success(request, 'User address updated')
			return redirect(reverse('core:address'))

		messages.warning(request, 'Fill the user address form appropriately')
		return redirect(reverse('core:address'))


class Settings(LoginRequiredMixin, Base):
	def get_request(self, request):
		user = request.user
		data_form = UserDataForm({'name': user.name, 'whatsapp_number': user.whatsapp_number, 'image': user.image, })
		password_form = UserPasswordForm(user=user)
		return (request, 'core/settings.html', {'data_form': data_form, 'password_form': password_form, 'nav_account': 'green'})


class UserData(LoginRequiredMixin, View):
	def get(self, request):
		return redirect(reverse('core:settings'))

	def post(self, request):
		form = UserDataForm(request.POST, request.FILES)
		if form.is_valid():
			user = User.objects.get(pk=request.user.id)
			user.name = form.cleaned_data.get('name')
			user.whatsapp_number = form.cleaned_data.get('whatsapp_number')
			if form.cleaned_data.get('image'):
				user.image = form.cleaned_data.get('image')
			user.save()
			messages.success(request, 'User data updated')
			return redirect(reverse('core:settings'))

		messages.warning(request, 'Fill the user form appropriately')
		return redirect(reverse('core:settings'))


class UserPassword(LoginRequiredMixin, View):
	def get(self, request):
		return redirect(reverse('core:settings'))

	def post(self, request):
		form = UserPasswordForm(request.POST, user=request.user)
		if form.is_valid():
			user = User.objects.get(pk=request.user.id)
			password = form.cleaned_data.get('password')
			user.password = password
			user.save()
			messages.success(request, 'User password updated')
			return redirect(reverse('core:settings'))

		messages.warning(request, 'Fill the password form appropriately')
		return redirect(reverse('core:settings'))

