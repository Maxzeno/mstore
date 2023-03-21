from django.urls import path
from .views import Settings, UserData, UserPassword, Address, UserAddress, Orders

app_name = 'core'

urlpatterns = [
    path('orders', Orders.as_view(), name='orders'),
    path('address', Address.as_view(), name='address'),
    path('address/data', UserAddress.as_view(), name='user_address'),
    path('settings', Settings.as_view(), name='settings'),
    path('settings/data', UserData.as_view(), name='user_data'),
    path('settings/password', UserPassword.as_view(), name='user_password'),
]
 