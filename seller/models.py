from django.db import models
from django.http import HttpResponseForbidden

# Create your models here.

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import redirect_to_login
from django.urls import reverse_lazy


class SellerRequiredMixin(LoginRequiredMixin):
    """
    Custom mixin that requires the user to be logged in, active, and a seller.
    """
    redirect_field_name = 'next'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not request.user.is_active:
            return redirect_to_login(
                self.request.get_full_path(),
                reverse_lazy('login'),
                self.redirect_field_name
            )
        if not request.user.is_seller: # assuming you have a field called "is_seller" on the User model
            return HttpResponseForbidden() # or any other response you want to return for non-sellers
        return super().dispatch(request, *args, **kwargs)
