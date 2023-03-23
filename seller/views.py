from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.http import Http404
from core.models import Order, Product, SubCategory
from .models import SellerRequiredMixin
from main.views import Base
from .forms import ProductForm
from utils import paginate_page

# Create your views here.


class Dashboard(SellerRequiredMixin, Base):
	def get_request(self, request):
		num_products = Product.objects.filter(seller=request.user.id).count()
		orders = Order.objects.filter(product__seller=request.user.id)[:5]
		num_buyers = orders.values('buyer').distinct().count()

		return (request, 'seller/dashboard.html', {
			'orders': orders, 
			'num_products': num_products,
			'num_buyers': num_buyers,
			'nav_seller': 'green',
		})


class OrderDetail(SellerRequiredMixin, Base):
	def get_request(self, request, pk):
		order = get_object_or_404(Order, pk=pk, product__seller=request.user.id)
		return (request, 'seller/order_detail.html', {
			'order': order,
			'nav_seller': 'green',
		})


class Orders(SellerRequiredMixin, Base):
	def get_request(self, request):
		orders = Order.objects.filter(product__seller=request.user.id)

		return (request, 'seller/orders.html', {
			**paginate_page(orders, request, Http404, obj='orders'),
			'nav_seller': 'green',
		})

class DeleteProduct(SellerRequiredMixin, Base):
	def get_request(self, request, pk):
		return redirect(reverse('seller:products'))

	def post_request(self, request, pk):
		print(request.POST)
		try:
			Product.objects.get(pk=pk).delete()
			messages.success(request, 'Product deleted successfully')
			return redirect(reverse('seller:products'))
		except Product.DoesNotExist:
			messages.warning(request, 'Product not deleted')
			return redirect(reverse('seller:products'))


class Products(SellerRequiredMixin, Base):
	def get_request(self, request):
		products = Product.objects.filter(seller=request.user.id).order_by('ordered')
		return (request, 'seller/products.html', {
			**paginate_page(products, request, Http404, obj='products'),
			'nav_seller': 'green',
		})


class CreateProduct(SellerRequiredMixin, Base):
	def get_request(self, request):
		form = ProductForm()
		return (request, 'seller/create_product.html', {'form': form, 'nav_seller': 'green',})

	def post_request(self, request):
		form = ProductForm(request.POST, request.FILES)
		if form.is_valid() and form.cleaned_data.get('sub_category'):
			product = Product()
			product.name = form.cleaned_data.get('name')
			product.state = form.cleaned_data.get('state')
			product.price = form.cleaned_data.get('price')
			product.sub_category = SubCategory.objects.get(pk=form.cleaned_data.get('sub_category'))
			product.description = form.cleaned_data.get('description')
			if form.cleaned_data.get('image'):
				product.image = form.cleaned_data.get('image')
			product.seller = request.user
			product.save()
			messages.success(request, 'Product created successfully')
			form = ProductForm()
			return (request, 'seller/create_product.html', {'form': form})

		messages.warning(request, 'Fill the product form appropriately')
		return (request, 'seller/create_product.html', {'form': form})


class UpdateProduct(SellerRequiredMixin, Base):
	def get_request(self, request, pk):
		product = get_object_or_404(Product, pk=pk, seller=request.user.id)
		product_dict = model_to_dict(product)
		del product_dict['ordered']
		del product_dict['is_approved']
		del product_dict['date']
		del product_dict['id']
		form = ProductForm(product_dict)
		return (request, 'seller/update_product.html', {
			'form': form,
			'nav_seller': 'green',
		})

	def post_request(self, request, pk):
		product = get_object_or_404(Product, pk=pk, seller=request.user.id)
		form = ProductForm(request.POST, request.FILES)
		if form.is_valid():
			product.name = form.cleaned_data.get('name')
			product.state = form.cleaned_data.get('state')
			product.price = form.cleaned_data.get('price')
			product.sub_category = SubCategory.objects.get(pk=form.cleaned_data.get('sub_category'))
			product.description = form.cleaned_data.get('description')
			if form.cleaned_data.get('image'):
				product.image = form.cleaned_data.get('image')
			product.save()
			messages.success(request, 'Product updated successfully')
			return redirect(reverse('seller:dashboard'))
		form = ProductForm(instance=product)
		messages.warning(request, 'Fill the product form appropriately')
		return (request, 'seller/update_product.html', {'form': form})
