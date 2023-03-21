from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.contrib import messages
from core.models import Order, Product
from .models import SellerRequiredMixin
from main.views import Base

# Create your views here.


class Dashboard(SellerRequiredMixin, Base):
	def get_request(self, request):
		num_products = Product.objects.filter(seller=request.user.id).count()
		orders = Order.objects.filter(product__seller=request.user.id)
		num_buyers = orders.values('buyer').distinct().count()

		return (request, 'seller/dashboard.html', {
			'orders': orders, 
			'num_products': num_products,
			'num_buyers': num_buyers
		})


# class UserAddress(LoginRequiredMixin, View):
# 	def get(self, request):
# 		return redirect(reverse('core:address'))

# 	def post(self, request):
# 		form = AddressForm(request.POST)
# 		if form.is_valid():
# 			user = User.objects.get(pk=request.user.id)
# 			user.state = form.cleaned_data.get('state')
# 			user.address = form.cleaned_data.get('address')
# 			user.save()
# 			messages.success(request, 'User address updated')
# 			return redirect(reverse('core:address'))

# 		messages.warning(request, 'Fill the user address form appropriately')
# 		return redirect(reverse('core:address'))
