from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.db.utils import IntegrityError
from django.contrib import messages
from django.http import Http404
from django.db.models import Q
from django.shortcuts import get_object_or_404
from core.models import Category, SubCategory, Product, User, Email, ContactUs as ContactUsModel
from utils import popular_categories, popular_categories_and_sub, paginate_page, is_mobile
from .forms import EmailForm, ContactUsForm

# Create your views here.


class Base(View):
	base_context = {**popular_categories()}

	def get(self, request, *args, **kwargs):
		request_obj, template, context = self.get_request(request, *args, **kwargs)
		context.update(self.base_context)
		return render(request_obj, template, context)

	def post(self, request, *args, **kwargs):
		data = self.post_request(request, *args, **kwargs)
		return render(*data)


class Index(Base):
	def get_request(self, request):
		is_mobile_device = is_mobile(request)
		if is_mobile_device:
			no_products  = 8
		else:
			no_products = 12

		products = Product.objects.filter(is_approved=True).order_by('ordered')[:no_products]
		return (request, 'main/index.html', {'products': products, 'email_form': EmailForm()})


class ProductDetail(Base):
	def get_request(self, request, pk):
		product = get_object_or_404(Product, pk=pk)
		is_mobile_device = is_mobile(request)
		if is_mobile_device:
			no_products  = 4
		else:
			no_products = 6

		related_products = Product.objects\
		.filter(Q(sub_category=product.sub_category) & Q(is_approved=True))\
		.exclude(pk=product.pk).order_by('ordered')[:no_products]

		return (request, 'main/product_detail.html', {'product': product, 'products': related_products})

class Products(Base):
	def get_request(self, request):
		category_name = request.GET.get('category')
		sub_name = request.GET.get('sub')
		seller_id = request.GET.get('seller')
		search = request.GET.get('search')

		category = None
		sub_category = None
		seller = None
		agrs = ''

		if not search:

			if seller_id:
				seller = User.objects.filter(pk=seller_id).first()

			if category_name and sub_name:
				category = Category.objects.filter(name=category_name).first()
				sub_category = SubCategory.objects.filter(Q(name=sub_name) & Q(category=category)).first()

			elif category_name:
				category = Category.objects.filter(name=category_name).first()


			if sub_category and seller:
				agrs += f'&category={category_name}&sub={sub_name}&seller={seller_id}'
				the_products = Product.objects.filter(Q(sub_category=sub_category) & Q(seller=seller) & Q(is_approved=True)).order_by('ordered')
			elif category and seller:
				agrs += f'&category={category_name}&sub={sub_name}&seller={seller_id}'
				the_products = Product.objects.filter(Q(sub_category__category=category) & Q(seller=seller) & Q(is_approved=True)).order_by('ordered')
			elif sub_category:
				agrs += f'&category={category_name}&sub={sub_name}'
				the_products = Product.objects.filter(Q(sub_category=sub_category) & Q(is_approved=True)).order_by('ordered')
			elif seller:
				agrs += f'&seller={seller_id}'
				the_products = Product.objects.filter(Q(seller=seller) & Q(is_approved=True)).order_by('ordered')
			elif category:
				agrs += f'&category={category_name}'
				the_products = Product.objects.filter(Q(sub_category__category=category) & Q(is_approved=True)).order_by('ordered')
			else:
				the_products = Product.objects.filter(is_approved=True).order_by('ordered')
		else:
			the_products = Product.objects.filter(Q(is_approved=True) & Q(name__icontains=search)).order_by('ordered')[:12]

		context = {
			**paginate_page(the_products, request, Http404),
			**popular_categories_and_sub(),
			'number_of_products': len(the_products),
			'url_args': agrs,
		}

		if seller:
			context['seller'] = seller_id
			context['seller_name'] = seller.name or "N/A"

		return (request, 'main/products.html', context)


class ContactUs(Base):
	def get_request(self, request):
		form = ContactUsForm()
		return (request, 'main/contact_us.html', {'form': form})

	def post_request(self, request):
		form = ContactUsForm(request.POST)
		if form.is_valid():
			try:
				ContactUsModel.objects.create(email=form.cleaned_data.get('email'), message=form.cleaned_data.get('message'))
				messages.success(request, 'Message has been received')
				form = ContactUsForm()
				return (request, 'main/contact_us.html', {'form': form})

			except IntegrityError:
				messages.warning(request, 'Fill email and message appropriately')
				return (request, 'main/contact_us.html', {'form': form})


		messages.warning(request, 'Fill email and message appropriately')
		return (request, 'main/contact_us.html', {'form': form})


class EmailSubscribe(View):
	def get(self, request):
		return redirect(reverse('main:index'))

	def post(self, request):
		email_form = EmailForm(request.POST)
		if email_form.is_valid():
			try:
				Email.objects.create(email=email_form.cleaned_data.get('email'))
				messages.success(request, 'Email address has been added')
				return redirect(reverse('main:index'))

			except IntegrityError:
				messages.warning(request, 'Email address is invalid or already exists')
				return redirect(reverse('main:index'))


		messages.warning(request, 'Email address is invalid or already exists')
		return redirect(reverse('main:index'))
