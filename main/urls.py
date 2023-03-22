from django.urls import path
from .views import Index, Products, ProductDetail, EmailSubscribe, ContactUs, BecomeSeller

app_name = 'main'

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('become-seller', BecomeSeller.as_view(), name='become_seller'),
    path('email-subscribe', EmailSubscribe.as_view(), name='email_subscribe'),
    path('contact-us', ContactUs.as_view(), name='contact_us'),
    path('products', Products.as_view(), name='products'),
    path('products/<str:pk>', ProductDetail.as_view(), name='product_detail'),
]
