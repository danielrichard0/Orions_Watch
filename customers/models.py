from django.db import models
from django.contrib.auth.models import User

class Province(models.Model):
    name = models.CharField('Nama Provinsi', max_length=150)

    def __str__(self):
        return self.name
    def get_province_choices(self):
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
    
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE, null=True, blank=True)
    village = models.ForeignKey(Villages, on_delete=models.CASCADE, null=True, blank=True)



