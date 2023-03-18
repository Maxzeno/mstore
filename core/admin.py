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
    fields = ('name', 'email', 'whatsapp_number', 'password', 'description', 'image', 'is_superuser', 'is_active', 'is_suspended', 'is_seller')
    list_display = ('name', 'email', 'whatsapp_number', 'is_superuser', 'is_active', 'is_suspended', 'is_seller', 'date_joined')
    order = ('name',)
    search_fields = ('name', 'email')
    list_filter = ('is_superuser', 'is_active', 'is_suspended', 'is_seller', 'date_joined')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'date')
    search_fields = ('name',)
    exclude = ('date', 'ordered')
    list_filter = ('date',)


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'category', 'date')
    search_fields = ('name',)
    exclude = ('date', 'ordered')
    list_filter = ('category', 'date')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    fields = ('id', 'name', 'description', 'image', 'sub_category', 'price', 'seller', 'is_approved')
    list_display = ('id', 'name', 'sub_category', 'price', 'seller', 'is_approved', 'date')
    search_fields = ('name',)
    exclude = ('date', 'ordered')
    readonly_fields = ('id',)
    list_filter = ('is_approved', 'sub_category', 'price', 'seller', 'date')
