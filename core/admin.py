from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.html import format_html
from django_summernote.models import Attachment
from ckeditor.widgets import CKEditorWidget

# from django_summernote.widgets import SummernoteWidget

from .models import User, Category, SubCategory, Product, Order, Email, ContactUs

# Register your models here.

admin.site.site_title = 'Nime enterprise Admin'
admin.site.index_title = 'Welcome to Nime enterprise'
admin.site.site_header = format_html('<a href="/adminuser/admin/"><img src="/static/img/icon nobg-crop.png" style="height: 100px"></a>')

admin.site.unregister(Group)
admin.site.unregister(Attachment)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fields = ('name', 'email', 'whatsapp_number', 'password', 'description', 'state', 'address', 'image', 'is_superuser', 'is_active', 'is_suspended', 'is_seller')
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
    fields = ('id', 'name', 'description', 'state', 'image', 'sub_category', 'price', 'seller', 'is_approved')
    list_display = ('id', 'name', 'sub_category', 'state', 'price', 'seller', 'is_approved', 'date')
    search_fields = ('name','id')
    exclude = ('ordered',)
    readonly_fields = ('id',)
    list_filter = ('is_approved', 'sub_category', 'state', 'price', 'seller', 'date')
    formfield_overrides = {
        'RichTextField': {'widget': CKEditorWidget}
    }


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    fields = ('id', 'product', 'buyer', 'status', 'date')
    list_display = ('id', 'product', 'buyer', 'status', 'date')
    search_fields = ('id', 'product', 'buyer')
    readonly_fields = ('id',)
    list_filter = ('status', 'product', 'buyer', 'date')


@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    list_display = ('email', 'date')
    search_fields = ('email',)
    list_filter = ('date',)


@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_resolved', 'date')
    search_fields = ('email',)
    list_filter = ('is_resolved', 'date')


