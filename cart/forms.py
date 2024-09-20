from django import forms
from django.shortcuts import get_object_or_404
from customers.models import Province, City, District, Villages, Address

# form pembayaran

class CityChoiceField(forms.ChoiceField):
    widget=forms.Select(attrs={'class' : 'form-control', 'id' : 'select-city', 'required': True})
    # choices=[('', 'Pilih Kota/Kabupaten')]

    def valid_value(self, value):
        return True

class DistrictChoiceField(forms.ChoiceField):
    widget=forms.Select(attrs={'class' : 'form-control', 'id' : 'select-district', 'required': True})
    # choices=[('', 'Pilih Kecamatan')]

    def valid_value(self, value):
        return True
    
class VillageChoiceField(forms.ChoiceField):
    widget=forms.Select(attrs={'class' : 'form-control', 'id' : 'select-village', 'required': False})
    required=False
    # choices=[('', 'Pilih Desa/Kelurahan')]

    def valid_value(self, value):
        return True


class TransactionForm(forms.ModelForm):
    first_name = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Nama Depan', 'required' : True}))
    last_name = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Nama Belakang', 'required' : True}))
    email = forms.EmailField(
        max_length=100,
        help_text='Isi dengan format email yang benar cth : (daniel@gmail.com)',
        widget=forms.EmailInput(
            attrs={
                'class':'form-control mb-3',
                'placeholder': 'Email',
                'required': True
            }
        )
    )

    model = Province()
    province = forms.ChoiceField(choices=model.get_province_choices(), widget=forms.Select(attrs={'class' : 'form-control', 'id' : 'select-province', 'required': True}), initial='')
    city = CityChoiceField()
    district = DistrictChoiceField()
    village = VillageChoiceField()
    alamat = forms.CharField(max_length=250, widget=forms.Textarea(attrs={'class' : 'form-control', 'placeholder' : 'Alamat', 'required': True}))
    post_code = forms.CharField(max_length=250, widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Kode Pos', 'required': True}))
    cust_note = forms.CharField(max_length=250, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder' : 'Catatan order (jika ada)', 'required' : False}))

    class Meta:
        model = Address
        fields = ['province', 'city', 'district', 'village', 'alamat', 'post_code', 'cust_note']

    def clean(self):
        cleaned_data = super().clean()

        province = cleaned_data.get('province')
        city = cleaned_data.get('city')
        district = cleaned_data.get('district')
        village = cleaned_data.get('village')

        try:
            cleaned_data['province'] = Province.objects.get(pk=province)
        except Province.DoesNotExist:
            self.add_error('province', "provinsi tidak ada") 

        try:
            cleaned_data['city'] = City.objects.get(pk=city)
        except City.DoesNotExist:
            self.add_error('city', "kota/kabupaten tidak ada") 

        try:
            cleaned_data['district'] = District.objects.get(pk=district)
        except District.DoesNotExist:
            self.add_error('district', "kecamatan tidak ada") 

        try:
            cleaned_data['village'] = Villages.objects.get(pk=village)
        except Villages.DoesNotExist:
            self.add_error('village', "Desa/kelurahan tidak ada") 

        print("cleaned_data : ", cleaned_data)
        return cleaned_data

    # additional = forms.CharField(max_length=250, widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Tambahan'}))
