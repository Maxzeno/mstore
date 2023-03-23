from django.db import models
from django.utils.translation import gettext_lazy as _
from django.apps import apps
from django.utils import timezone
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.hashers import (
    check_password, is_password_usable, make_password,
)
from ckeditor.fields import RichTextField
### from django_summernote.fields import SummernoteTextField


import shortuuid


# Create your models here.

class MyUserManager(BaseUserManager):
	use_in_migrations = True

	def _create_user(self, email, password, **extra_fields):
		"""
		Create and save a user with the given, email, and password.
		"""
		email = self.normalize_email(email)
		user = self.model(email=email, password=password, **extra_fields)
		user.save(using=self._db)
		return user

	def create(self, email=None, password=None, **extra_fields):
		extra_fields.setdefault('is_staff', extra_fields.get('is_seller'))
		extra_fields.setdefault('is_superuser', False)
		return self._create_user(email, password, **extra_fields)


	def create_user(self, email=None, password=None, **extra_fields):
		extra_fields.setdefault('is_staff', extra_fields.get('is_seller'))
		extra_fields.setdefault('is_superuser', False)
		return self._create_user(email, password, **extra_fields)

	def create_superuser(self, email=None, password=None, **extra_fields):
		extra_fields.setdefault('is_staff', True)
		extra_fields.setdefault('is_superuser', True)
		extra_fields.setdefault('is_seller', True)

		if extra_fields.get('is_staff') is not True:
			raise ValueError('Superuser must have is_staff=True.')
		if extra_fields.get('is_superuser') is not True:
			raise ValueError('Superuser must have is_superuser=True.')

		return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(unique=True)
    whatsapp_number = models.CharField(max_length=30)
    image = models.ImageField(upload_to='images/', default='images/person.png', blank=True, null=True)
    _password = ''
    state = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=500, blank=True, null=True)
    description = models.CharField(max_length=1000, blank=True, null=True)
    is_staff = models.BooleanField(default=False, help_text=_('Designates whether the user can log into this admin site.'))
    is_active = models.BooleanField(default=True)
    is_seller = models.BooleanField(default=False)
    is_suspended = models.BooleanField(default=False)
    ordered = models.IntegerField(default=0)

    date_joined = models.DateTimeField(default=timezone.now)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = MyUserManager()

    def save(self, *args, **kwargs):
        u = self.__class__.objects.filter(pk=self.pk).first()
        if not u or u and u.password != self.password:
            self.set_password(self.password)
        super(User, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        swappable = 'AUTH_USER_MODEL'


    def __str__(self):
        return self.name or self.email


# class Address(models.Model):
#     state = models.CharField(max_length=100, blank=True, null=True)
#     address = models.CharField(max_length=500, blank=True, null=True)
#     # user = models.ForeignKey(User, on_delete=models.CASCADE)
#     date = models.DateTimeField(default=timezone.now)

#     def __str__(self):
#         return self.state or self.address[:20]

#     class Meta:
#         verbose_name_plural = 'Addresses'


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='images/', default='images/NA-removebg.png', blank=True, null=True)
    ordered = models.IntegerField(default=0)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'


class SubCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='images/', default='images/NA-removebg.png', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    ordered = models.IntegerField(default=0)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Sub Categories'

        constraints = [
            models.UniqueConstraint(
                fields=['category', 'name'],
                name='unique_name_per_category'
            )
        ]

        
def unique_id(table):
    while True:
        random = shortuuid.ShortUUID().random(length=8)
        if not table.objects.filter(id=random).exists():
            break
    return random

def product_id():
    return unique_id(Product)

def order_id():
    return unique_id(Order)


class Product(models.Model):
    id = models.CharField(primary_key=True, max_length=10, default=product_id)
    name = models.CharField(max_length=100)
    description = RichTextField(blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='images/', default='images/NA-removebg.png', blank=True, null=True)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.IntegerField(default=0)
    is_approved = models.BooleanField(default=False)
    date = models.DateTimeField(default=timezone.now)

    # DEFAULT_AUTO_FIELD = 'django.db.models.UUIDField'

    def __str__(self):
        return self.name

    def is_approved_status(self):
        if self.is_approved:
            return 'Approved'
        return 'Not Approved'
    

class Order(models.Model):
    STATUS_CHOICES = [
        ('S', 'Success'),
        ('P', 'Pending'),
        ('C', 'Cancel'),
    ]

    id = models.CharField(primary_key=True, max_length=10, default=order_id)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    has_paid = models.BooleanField(default=False)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')
    date = models.DateTimeField(default=timezone.now)

    def order_status(self):
        for i in self.STATUS_CHOICES:
            if i[0].upper() == self.status.upper():
                return i[1]
        return ''

    def has_paid_status(self):
        if self.has_paid:
            return 'Yes'
        return 'No'

    def __str__(self):
        return self.id


class Email(models.Model):
    email = models.EmailField(unique=True, null=False)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.email
    

class ContactUs(models.Model):
    email = models.EmailField(unique=True)
    message = models.CharField(max_length=1000)
    date = models.DateTimeField(default=timezone.now)
    is_resolved = models.BooleanField(default=False)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name_plural = 'Contact us'
