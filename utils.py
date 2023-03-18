from core.models import Category, SubCategory

def popular_categories():
	categories = Category.objects.order_by('ordered')[:12]
	return {'categories': categories}

def popular_categories_and_sub():
	categories = Category.objects.values('id', 'name')
	result = []
	for category in categories:
		result.append([
			category['name'],
			[ data[0] for data in SubCategory.objects.filter(category=category['id']).values_list('name') ]
		])
	return result
