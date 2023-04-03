from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import User, Order, Product, Cart as CartModel
from .forms import UserDataForm, UserPasswordForm, AddressForm
from main.views import Base
# Create your views here.


class Cart(LoginRequiredMixin, Base):
	def get_request(self, request):
		items = CartModel.objects.filter(buyer=request.user, checked_out=False)
		total = 0
		for item in items:
			total += item.total_price()
		return (request, 'core/cart.html', {'cart_items': items, 'total': total, 'nav_account': 'green'})


class CartPlus(LoginRequiredMixin, Base):
	def get_request(self, request, pk):
		product = Product.objects.filter(pk=pk).first()
		if not product or not product.is_approved:
			return JsonResponse({'ok': False})

		total = 0
		cart_item, created = CartModel.objects.get_or_create(buyer=request.user, product=product, checked_out=False)
		if not created:
			cart_item.quantity += 1
			cart_item.save()

			items = CartModel.objects.filter(buyer=request.user, checked_out=False)
			
			for item in items:
				total += item.total_price()
		return JsonResponse({'ok': True, 'price': cart_item.product.price, 'total': total, 'quantity': cart_item.quantity})


class CartMinus(LoginRequiredMixin, Base):
	def get_request(self, request, pk):
		product = Product.objects.filter(pk=pk).first()
		if not product:
			return JsonResponse({'ok': False})

		cart_item = CartModel.objects.filter(buyer=request.user, product=product, checked_out=False).first()
		if not cart_item:
			return JsonResponse({'ok': False}) 
		cart_item.quantity = cart_item.quantity -1 if cart_item.quantity > 0 else 0
		cart_item.save()

		items = CartModel.objects.filter(buyer=request.user, checked_out=False)
		total = 0
		for item in items:
			total += item.total_price()
		return JsonResponse({'ok': True, 'price': cart_item.product.price, 'total': total, 'quantity': cart_item.quantity})


class CartRemove(LoginRequiredMixin, Base):
	def get_request(self, request, pk):
		product = Product.objects.filter(pk=pk).first()
		if not product:
			return JsonResponse({'ok': False})

		cart_item = CartModel.objects.filter(buyer=request.user, product=product, checked_out=False).first()
		if not cart_item:
			return JsonResponse({'ok': False}) 
		cart_item.delete()
		return JsonResponse({'ok': True})


# lots of bugs
class OrderCreate(LoginRequiredMixin, Base):
	def get_request(self, request, pk):
		return redirect(reverse('core:order_detail', kwargs={'pk': pk}))

	def post_request(self, request, pk):
		# body
		# return redirect(reverse('core:order_detail', kwargs={'pk':order.pk}))
		pass


class OrderDetail(LoginRequiredMixin, Base):
	def get_request(self, request, pk):
		""" This order details creates an order if given product id"""
		order = Order.objects.filter(pk=pk).first()
		if order:
			return (request, 'core/order_detail.html', {'order': order, 'nav_account': 'green'})
		messages.warning(request, 'Click order if you want to continue your request')
		return redirect(reverse('main:product_detail', kwargs={'pk': pk}))


class Orders(LoginRequiredMixin, Base):
	def get_request(self, request):
		orders = Order.objects.filter(buyer=request.user.id)
		for order in orders:
			print(order.get_total_price_now())
		return (request, 'core/orders.html', {'orders': orders, 'nav_account': 'green'})


class Address(LoginRequiredMixin, Base):
	def get_request(self, request):
		user = request.user
		address_form = AddressForm({'state': user.state, 'address': user.address})
		return (request, 'core/address.html', {'address_form': address_form, 'nav_account': 'green'})

	def post_request(self, request):
		form = AddressForm(request.POST)
		if form.is_valid():
			user = User.objects.get(pk=request.user.id)
			user.state = form.cleaned_data.get('state')
			user.address = form.cleaned_data.get('address')
			user.save()
			messages.success(request, 'User address updated')
			return (request, 'core/address.html', {'address_form': form, 'nav_account': 'green'})

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

