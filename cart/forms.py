from django import forms
from customers.models import Province, City, District, Villages

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
    widget=forms.Select(attrs={'class' : 'form-control', 'id' : 'select-village', 'required': True})
    # choices=[('', 'Pilih Desa/Kelurahan')]

    def valid_value(self, value):
        return True


class TransactionForm(forms.Form):
    first_name = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Nama Depan', 'required' : True}))
    last_name = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Nama Belakang'}))
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
    province = forms.ChoiceField(choices=model.get_province_choices(), widget=forms.Select(attrs={'class' : 'form-control', 'id' : 'select-province', 'required': True}))
    city = CityChoiceField()
    district = DistrictChoiceField()
    village = VillageChoiceField()
    address = forms.CharField(max_length=250, widget=forms.Textarea(attrs={'class' : 'form-control', 'placeholder' : 'Alamat', 'required': True}))
    post_code = forms.IntegerField(widget=forms.NumberInput(attrs={'class' : 'form-control', 'placeholder' : 'Kode Pos', 'required': True}))
    additional_info = forms.CharField(max_length=250, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder' : 'Catatan order (jika ada)'}))

    # additional = forms.CharField(max_length=250, widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Tambahan'}))
