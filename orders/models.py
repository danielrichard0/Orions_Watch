from django.db import models
from django.contrib.auth.models import User
from customers.models import Address
import uuid

class Order(models.Model):
    first_name = models.CharField("Nama Depan", max_length=150, null=False, blank=False)
    last_name = models.CharField("Nama Belakang", max_length=150, null=False, blank=False)  
    email = models.CharField("Alamat Email", max_length=250, null=False, blank=False)
    address = models.ForeignKey(Address, null=True,on_delete=models.SET_NULL)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    date_created = models.DateTimeField("Date Created",auto_now_add=True) 
    ongkir = models.IntegerField("Harga Ongkos Kirim", null=True, blank=True)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    is_guest = models.BooleanField("Apakah Pesanan Guest", null=False, blank=False)
    cust_note = models.CharField("Catatan Customer", max_length=250, null=True, blank=True)

