from django.urls import path
from .views import Dashboard, Products, CreateProduct, UpdateProduct, Orders, OrderDetail, DeleteProduct

app_name = 'seller'

urlpatterns = [
    path('dashboard', Dashboard.as_view(), name='dashboard'),
    path('orders', Orders.as_view(), name='orders'),
    path('orders/<str:pk>', OrderDetail.as_view(), name='order_detail'),
    path('products', Products.as_view(), name='products'),
    path('products/create', CreateProduct.as_view(), name='create_products'),
    path('products/update/<str:pk>', UpdateProduct.as_view(), name='update_products'),
    path('products/delete/<str:pk>', DeleteProduct.as_view(), name='delete_products'),
]
 