from django.urls import path
from .views import Dashboard

app_name = 'seller'

urlpatterns = [
    path('dashboard', Dashboard.as_view(), name='dashboard'),
]
 