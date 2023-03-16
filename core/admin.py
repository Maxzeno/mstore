from django.contrib import admin
from django.contrib.auth.models import Group
from .models import User, Category, SubCategory, Product

# Register your models here.

admin.site.site_title = 'Mstore Admin'
admin.site.index_title = 'Welcome to Mstore'
# admin.site.site_header = format_html('<a href="/adminuser/admin/"><img src="/static/images/logo.png" style="height: 100px"></a>')

admin.site.unregister(Group)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fields = ('name', 'email', 'whatsapp_number', 'password', 'is_superuser', 'is_active', 'is_seller')
    list_display = ('name', 'email', 'is_superuser', 'is_active', 'is_seller', 'date_joined')
    order = ('name',)
    search_fields = ('name', 'email')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'date')
    search_fields = ('name',)
    exclude = ('date',)


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'date')
    search_fields = ('name',)
    exclude = ('date',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'sub_category', 'price', 'seller', 'date')
    search_fields = ('name',)
    exclude = ('date',)