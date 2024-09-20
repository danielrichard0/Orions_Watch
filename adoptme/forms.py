
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

class CustomLoginForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class' : 'form-control', 'placeholder': 'password'}))

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("Invalid username or password")
        return cleaned_data

class CustomRegistrationForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class':'form-control mb-3',
                'placeholder': 'Nama depan'
            }
        )
    )

    last_name = forms.CharField(
        max_length=100,        
        widget=forms.TextInput(
            attrs={
                'class':'form-control mb-3',
                'placeholder': 'Nama Belakang'
            }
        )
    )

    username = forms.CharField(
        max_length=100,
        help_text='''Wajib. Minimal 10 karakter. Hanya huruf, angka, dan @/./+/-/_.
        ''',
        widget=forms.TextInput(
            attrs={
                'class':'form-control mb-3',
                'placeholder': 'Username'
            }
        )
    )

    email = forms.EmailField(
        max_length=100,
        help_text='Isi dengan format email yang benar cth : (daniel@gmail.com)',
        widget=forms.EmailInput(
            attrs={
                'class':'form-control mb-3',
                'placeholder': 'Email'
            }
        )
    )

    password = forms.CharField(
        max_length=100,
        widget=forms.PasswordInput(
            attrs={
                'class':'form-control mb-3',
                'placeholder': 'Password'
            }
        )
    )

    confirm_password = forms.CharField(
        max_length=100,
        help_text="Ulangi password yang anda input",
        widget=forms.PasswordInput(
            attrs={
                'class':'form-control mb-3',
                'placeholder': 'Konfirmasi password'
            }
        )
    )


    class Meta:
        model = User
        fields = [ 'first_name', 'last_name', 'username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')
        
        email_check = User.objects.filter(email=email)
        if email_check.exists():
            raise forms.ValidationError("Email sudah terdaftar, silahkan gunakan email yang lain, atau login menggunakan akun yang sudah terdaftar")

        if len(username) < 10:
            self.add_error('username', "Username tidak boleh kurang dari 10 karakter")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Password tidak cocok, silahkan ulangi kembali")

        return cleaned_data
