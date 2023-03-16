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
    fields = ('name', 'email', 'whatsapp_number', 'password', 'is_superuser', 'is_active', 'is_suspended', 'is_seller')
    list_display = ('name', 'email', 'whatsapp_number', 'is_superuser', 'is_active', 'is_suspended', 'is_seller', 'date_joined')
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
    fields = ('id', 'name', 'description', 'image', 'sub_category', 'price', 'seller', 'is_approved')
    list_display = ('id', 'name', 'sub_category', 'price', 'seller', 'is_approved', 'date')
    search_fields = ('name',)
    exclude = ('date',)
    readonly_fields = ('id',)
