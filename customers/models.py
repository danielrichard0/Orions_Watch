from django.db import models
from django.contrib.auth.models import User

class Province(models.Model):
    name = models.CharField('Nama Provinsi', max_length=150)

    def __str__(self):
        return self.name
    def get_province_choices():
        provinces = Province.objects.all()
        prv_choices = [('', 'Pilih Provinsi')]
        for prv in provinces:
            prv_choices.append((prv.id, prv.name))

        return prv_choices
        
    
class City(models.Model):
    name = models.CharField('Nama Kabupaten/Kota', max_length=150)
    province = models.ForeignKey(Province, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
class District(models.Model):
    name = models.CharField('Nama Kecamatan', max_length=150, null=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
class Villages(models.Model):
    name = models.CharField('Nama Desa', max_length=150,null=True, blank=True)
    district = models.ForeignKey(District, null=True, blank=True, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
   
class Address(models.Model):
    first_name = models.CharField('Nama Depan', max_length=50, null=True, blank=True)
    last_name = models.CharField('Nama Belakang', max_length=50, null=True, blank=True)
    email = models.CharField('Email', max_length=250, null=True, blank=True)
    phone_number = models.CharField('Nomor Telpon', max_length=15, null=True, blank=True)
    province = models.ForeignKey(Province, null=False, blank=False, on_delete=models.RESTRICT)
    city = models.ForeignKey(City, null=False, blank=False, on_delete=models.RESTRICT)
    district = models.ForeignKey(District, null=False, blank=False, on_delete=models.RESTRICT)
    village = models.ForeignKey(Villages, null=False, blank=False, on_delete=models.RESTRICT)
    alamat = models.CharField('Alamat Kirim', max_length=250, null=False)
    post_code = models.CharField('Kode Pos', max_length=10, null=False)
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        string = f"{self.alamat} \n{self.village} \n{self.district} \n{self.city} \n{self.province} \n{self.post_code}"
        return string

    

    



