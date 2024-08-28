from django.db import models
import datetime
import django.utils.timezone

# Create your models here.
class Product(models.Model):
    title = models.CharField("Title",max_length=50)
    description = models.CharField("Description",max_length=200)
    active = models.BooleanField("Active",default=False)
    price = models.IntegerField("Price",default=0)
    stock = models.IntegerField("Stock",default=0)
    discount = models.IntegerField("Discount",default=0)
    date_created = models.DateTimeField("Date Created",auto_now_add=True)
    image = models.ImageField(null=True,blank=True ,upload_to="images/product/")

    def __str__(self):
        return self.title

