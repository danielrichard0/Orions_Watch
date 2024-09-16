from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib.auth import login, authenticate, logout
from products.models import Product
from cart.models import Cart
from django.conf import settings
from django.db.models import Sum, F
from .forms import CustomLoginForm, CustomRegistrationForm


def index(request):
    all_product = Product.objects.filter(image__isnull=False)[:8]
    packet = {"products" : all_product}
    return render(request, "index.html", packet)

def custom_login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_staff : 
                    return redirect('/admin/')
                else : 
                    return redirect('/')
            else:
                form.add_error(None, "Invalid username or password")
    else:
        if request.user.is_authenticated:
            return render(request, 'profile.html/')
        form = CustomLoginForm()

    return render(request, 'login.html', {'form' : form})

def custom_registration_view(request):
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            input_email = form.cleaned_data['email']
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('/')
    else : 
        form = CustomRegistrationForm()
    return render(request, 'registration-page.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('/')