from django.db import models
from django.contrib.auth.models import User
from products.models import Product

class Cart(models.Model):
    session_id = models.CharField('Session ID', max_length=500, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField("Quantity", default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField("Date Created",auto_now_add=True)
    
    @property
    def total_itemprice(self):
        return self.product.price * self.quantity

    def __str__(self):
        return self.session_id