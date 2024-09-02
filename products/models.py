from django.db import models
from django.template.defaultfilters import slugify
import datetime
import django.utils.timezone


# Create your models here.
class Category(models.Model):
    name = models.CharField("Name", max_length=50, unique=True)
    date_created = models.DateTimeField("Date Created",auto_now_add=True)
    description = models.TextField("Description")
    active = models.BooleanField("Active",default=True)
    slug = models.CharField("Content Slug", max_length=50, blank=True, unique=True, editable=False) 

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Product(models.Model):
    title = models.CharField("Title",max_length=50)
    description = models.CharField("Description",max_length=200)
    active = models.BooleanField("Active",default=False)
    price = models.IntegerField("Price",default=0, null=False)
    stock = models.IntegerField("Stock",default=0)
    discount = models.IntegerField("Discount",default=0)
    date_created = models.DateTimeField("Date Created",auto_now_add=True)
    image = models.ImageField(null=True,blank=True ,upload_to="images/product/")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    



