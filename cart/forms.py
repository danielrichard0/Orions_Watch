from django import forms
from django.shortcuts import get_object_or_404
from customers.models import  District, Villages, Address, ProvinceRajaOngkir, CityRajaOngkir
from django.contrib.auth.models import User

# form pembayaran

class CityChoiceField(forms.ChoiceField):
    def __init__(self, province_id=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        widget=forms.Select(attrs={'class' : 'form-control', 'id' : 'select-city', 'required': True})
        if province_id:
            get_cities = CityRajaOngkir.objects.filter(province=province_id)
            choices = []
            for city in get_cities:
                choices.append((city.id, city.city_name))
            widget=forms.Select(attrs={'class' : 'form-control', 'id' : 'select-city', 'required': True}, choices=choices)
        self.widget=widget


    def valid_value(self, value):
        return True

# class DistrictChoiceField(forms.ChoiceField):
#     def __init__(self, city_id=None, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         widget=forms.Select(attrs={'class' : 'form-control', 'id' : 'select-district', 'required': True})
#         if city_id:
#             get_districts = District.objects.filter(city=city_id)
#             choices = []
#             for district in get_districts:
#                 choices.append((district.id, district.name))
#             widget=forms.Select(attrs={'class' : 'form-control', 'id' : 'select-district', 'required': True}, choices=choices)
#         self.widget=widget


#     def valid_value(self, value):
#         return True
    
# class VillageChoiceField(forms.ChoiceField):
#     def __init__(self, district_id=None, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         widget=forms.Select(attrs={'class' : 'form-control', 'id' : 'select-village', 'required': True})
#         if district_id:
#             get_villages = Villages.objects.filter(district=district_id)
#             choices = []
#             for vill in get_villages:
#                 choices.append((vill.id, vill.name))
#             print("choices : ", choices)
#             widget=forms.Select(attrs={'class' : 'form-control', 'id' : 'select-village', 'required': True}, choices=choices)
#         self.widget=widget



#     def valid_value(self, value):
#         return True
    
class AddressForm(forms.ModelForm):
    def __init__(self, address=None,user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if (address):
            self.fields['province'] = forms.ChoiceField(choices=ProvinceRajaOngkir.get_province_choices(), widget=forms.Select(attrs={'class' : 'form-control', 'id' : 'select-province', 'required': True}), initial=address.province.id)
            # self.fields['village'] = VillageChoiceField(district_id=address.district.id, initial=address.village.id)
            # self.fields['district'] = DistrictChoiceField(city_id=address.city.id, initial=address.district.id)
            self.fields['city'] = CityChoiceField(province_id=address.province.id, initial=address.city.id)
            self.fields['first_name'] = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Nama Depan', 'required' : True, }), initial=address.first_name)
            self.fields['last_name'] = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Nama Belakang', 'required' : True, }), initial=address.last_name)
            self.fields['email'] = forms.EmailField(
                max_length=100, 
                help_text='Isi dengan format email yang benar cth : (daniel@gmail.com)',
                widget=forms.EmailInput(
                    attrs={
                        'class':'form-control mb-3',
                        'placeholder': 'Email',
                        'required': True,
                        
                    }
                ),
                initial=address.email
            )
            self.fields['phone_number'] = forms.CharField(
                max_length=15, 
                widget=forms.TextInput(
                    attrs={
                        'class':'form-control mb-3',
                        'placeholder': 'Nomor Telepon',
                        'required': True,                
                    }
                ),
                initial=address.phone_number
            )
            self.fields['alamat'] = forms.CharField(max_length=250, widget=forms.Textarea(attrs={'class' : 'form-control', 'placeholder' : 'Alamat', 'required': True}), initial=address.alamat)
            self.fields['post_code'] = forms.CharField(max_length=250, widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Kode Pos', 'required': True}), initial=address.post_code)
        else :
            self.fields['province'] = forms.ChoiceField(choices=ProvinceRajaOngkir.get_province_choices(), widget=forms.Select(attrs={'class' : 'form-control', 'id' : 'select-province', 'required': True}), initial='')
            # self.fields['village'] = VillageChoiceField()
            # self.fields['district'] = DistrictChoiceField()
            self.fields['city'] = CityChoiceField()
            self.fields['first_name'] = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Nama Depan', 'required' : True, }))
            self.fields['last_name'] = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Nama Belakang', 'required' : True, }))
            self.fields['email'] = forms.EmailField(
                max_length=100, 
                help_text='Isi dengan format email yang benar cth : (daniel@gmail.com)',
                widget=forms.EmailInput(
                    attrs={
                        'class':'form-control mb-3',
                        'placeholder': 'Email',
                        'required': True,
                        
                    }
                )        
            )
            self.fields['phone_number'] = forms.CharField(
                max_length=15, 
                widget=forms.TextInput(
                    attrs={
                        'class':'form-control mb-3',
                        'placeholder': 'Nomor Telepon',
                        'required': True,                
                    }
                )        
            )
            self.fields['alamat'] = forms.CharField(max_length=250, widget=forms.Textarea(attrs={'class' : 'form-control', 'placeholder' : 'Alamat', 'required': True}))
            self.fields['post_code'] = forms.CharField(max_length=250, widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Kode Pos', 'required': True}))

    class Meta:
        model = Address
        fields = ['first_name','last_name','email', 'phone_number','province', 'city', 'alamat', 'post_code']
    
    def clean(self):
        cleaned_data = super().clean()

        province = cleaned_data.get('province')
        city = cleaned_data.get('city')

        try:
            cleaned_data['province'] = ProvinceRajaOngkir.objects.get(pk=province)
        except ProvinceRajaOngkir.DoesNotExist:
            self.add_error('province', "provinsi tidak ada") 

        try:
            cleaned_data['city'] = CityRajaOngkir.objects.get(pk=city)
        except CityRajaOngkir.DoesNotExist:
            self.add_error('city', "kota/kabupaten tidak ada") 

        print("clean_data : ", cleaned_data)

        # try:
        #     cleaned_data['district'] = District.objects.get(pk=district)
        # except District.DoesNotExist:
        #     self.add_error('district', "kecamatan tidak ada") 

        # if not village:
        #     return cleaned_data
        # else:
        #     try:
        #         cleaned_data['village'] = Villages.objects.get(pk=village)
        #     except Villages.DoesNotExist:
        #         self.add_error('village', "Desa/kelurahan tidak ada") 

        return cleaned_data

class TransactionForm(AddressForm):
    def __init__(self, address=None, user=None, *args, **kwargs):
        super().__init__(address, user, *args, **kwargs)

    cust_note = forms.CharField(max_length=250, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder' : 'Catatan order (jika ada)'}), required=False)
    is_save = forms.BooleanField(widget=forms.CheckboxInput(attrs={ 'class':'form-check-input','required' : False}), label="Simpan Alamat?", required=False)




# class TransactionForm(forms.ModelForm):
#     first_name = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Nama Depan', 'required' : True}))
#     last_name = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Nama Belakang', 'required' : True}))
#     email = forms.EmailField(
#         max_length=100,
#         help_text='Isi dengan format email yang benar cth : (daniel@gmail.com)',
#         widget=forms.EmailInput(
#             attrs={
#                 'class':'form-control mb-3',
#                 'placeholder': 'Email',
#                 'required': True
#             }
#         )
#     )

#     model = Province()
#     province = forms.ChoiceField(choices=model.get_province_choices(), widget=forms.Select(attrs={'class' : 'form-control', 'id' : 'select-province', 'required': True}), initial='')
#     city = CityChoiceField()
#     district = DistrictChoiceField()
#     village = VillageChoiceField()
#     alamat = forms.CharField(max_length=250, widget=forms.Textarea(attrs={'class' : 'form-control', 'placeholder' : 'Alamat', 'required': True}))
#     post_code = forms.CharField(max_length=250, widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Kode Pos', 'required': True}))
#     cust_note = forms.CharField(max_length=250, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder' : 'Catatan order (jika ada)', 'required' : False}), required=False)
#     user = None

#     class Meta:
#         model = Address
#         fields = ['province', 'city', 'district', 'village', 'alamat', 'post_code']

#     def clean(self):
#         cleaned_data = super().clean()

#         province = cleaned_data.get('province')
#         city = cleaned_data.get('city')
#         district = cleaned_data.get('district')
#         village = cleaned_data.get('village')

#         try:
#             cleaned_data['province'] = Province.objects.get(pk=province)
#         except Province.DoesNotExist:
#             self.add_error('province', "provinsi tidak ada") 

#         try:
#             cleaned_data['city'] = City.objects.get(pk=city)
#         except City.DoesNotExist:
#             self.add_error('city', "kota/kabupaten tidak ada") 

#         try:
#             cleaned_data['district'] = District.objects.get(pk=district)
#         except District.DoesNotExist:
#             self.add_error('district', "kecamatan tidak ada") 

#         if not village:
#             return cleaned_data
#         else:
#             try:
#                 cleaned_data['village'] = Villages.objects.get(pk=village)
#             except Villages.DoesNotExist:
#                 self.add_error('village', "Desa/kelurahan tidak ada") 

#         return cleaned_data

    # additional = forms.CharField(max_length=250, widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Tambahan'}))
