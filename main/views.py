from django.shortcuts import render
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from core.models import Category, Product 
from utils import popular_categories, popular_categories_and_sub
# Create your views here.

def index(request):
	print(popular_categories_and_sub())
	products = Product.objects.order_by('ordered')[:10]
	return render(request, 'main/index.html', {**popular_categories(), 'products': products})


def products(request):
	all_products = Product.objects.order_by('ordered')
	paginator = Paginator(all_products, 12)
	page_number = request.GET.get('page')

	try:
		page_obj = paginator.page(page_number)
	except PageNotAnInteger:
		page_obj = paginator.page(1)
	except EmptyPage:
		raise Http404("The resource you requested does not exist")

	page_list = page_obj.paginator.get_elided_page_range(page_obj.number, on_each_side=0, on_ends=1)

	return render(request, 'main/products.html', {
		**popular_categories(), 
		'categories_and_sub': popular_categories_and_sub(),
		'products': page_obj,
		'page_list': page_list,
	})
