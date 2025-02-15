from django.db import models
from django.contrib.auth.models import User
from customers.models import Address
import uuid

class Order(models.Model):
    status_choices = [
        ('MK1', 'Menunggu Konfirmasi'),
        ('DP2', 'Diproses'),
        ('SD3', 'Dikirim'),
        ('ST4', 'Sampai Tujuan')
    ]
    
    first_name = models.CharField("Nama Depan", max_length=150, null=False, blank=False)
    last_name = models.CharField("Nama Belakang", max_length=150, null=False, blank=False)  
    email = models.CharField("Alamat Email", max_length=250, null=False, blank=False)
    address = models.ForeignKey(Address, null=True,on_delete=models.SET_NULL, verbose_name="Alamat Penerima")
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, verbose_name="Pengguna Terkait")
    date_created = models.DateTimeField("Date Created",auto_now_add=True) 
    ongkir = models.IntegerField("Harga Ongkos Kirim", null=True, blank=True)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    is_guest = models.BooleanField("Apakah Pesanan Guest", null=False, blank=False)
    cust_note = models.CharField("Catatan Customer", max_length=250, null=True, blank=True)
    total_price = models.IntegerField("Harga Keseluruhan", null=False, blank=False)
    total_final = models.IntegerField("Harga Keseluruhan Tambah Ongkir", null=False, blank=False)
    status = models.CharField("Status Pesanan",max_length=3, choices=status_choices, null=False, blank=False)
    nomor_resi = models.CharField("Nomor Resi", max_length=50, null=True, blank=False)
    agen_pengiriman = models.CharField("Agen Pengiriman", max_length=50, null=True, blank=True)
    service_pengiriman = models.CharField("Service Pengiriman", max_length=50, null=True, blank=True)
    total_weight = models.IntegerField("Total Berat", null=True, blank=True)
    

    def __str__(self):
        date = self.date_created.strftime("%d/%B/%Y - %H:%M")
        string = f"{self.first_name} {self.last_name} {date}"
        return string
    
    

