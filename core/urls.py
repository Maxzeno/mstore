from django.urls import path
from .views import (Settings, UserData, UserPassword, Address, UserAddress, Orders, OrderDetail, OrderCreate,
		Cart, CartPlus, CartMinus, CartRemove)

app_name = 'core'

urlpatterns = [
    path('cart', Cart.as_view(), name='cart'),
    path('cart-plus/<str:pk>', CartPlus.as_view(), name='cart_plus'),
    path('cart-minus/<str:pk>', CartMinus.as_view(), name='cart_minus'),
    path('cart-remove/<str:pk>', CartRemove.as_view(), name='cart_remove'),
    path('orders', Orders.as_view(), name='orders'),
    path('order-detail/<str:pk>', OrderDetail.as_view(), name='order_detail'),
    path('order-create/<str:pk>', OrderCreate.as_view(), name='order_create'),
    path('address', Address.as_view(), name='address'),
    path('address/data', UserAddress.as_view(), name='user_address'),
    path('settings', Settings.as_view(), name='settings'),
    path('settings/data', UserData.as_view(), name='user_data'),
    path('settings/password', UserPassword.as_view(), name='user_password'),
]
 