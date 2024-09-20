from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from orders.models import Order
from django.contrib.sessions.models import Session


class Cart(models.Model):
    quantity = models.IntegerField("Quantity", default=1)
    session = models.ForeignKey(Session, null=True, blank=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField("Date Created",auto_now_add=True)
    order = models.ForeignKey(Order, null=True, blank=True, on_delete=models.CASCADE)
    
    @property
    def total_itemprice(self):
        return self.product.price * self.quantity

    def __str__(self):
        return self.session_id