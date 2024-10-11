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
from orders.models import Order
from django.db.models import Case,When,Value,CharField
from django.forms.models import model_to_dict
from cart.forms import TransactionForm, AddressForm
from django.contrib.auth.models import User
from customers.models import Address


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
            return redirect('/account/')
        form = CustomLoginForm()

    return render(request, 'login.html', {'form' : form})

def custom_registration_view(request):
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            # input_email = form.cleaned_data['email']
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('/')
    else : 
        form = CustomRegistrationForm()
    return render(request, 'registration-page.html', {'form': form})

def contact(request):
    if request.method == 'GET':
        return render(request, 'kontak.html')
    else:
        return HttpResponse("Invalid Method")

def logout_view(request):
    logout(request)
    return redirect('/')

def dashboard(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return render(request, 'profile/dashboard.html/')
        else:
            HttpResponse("Anda Belum Login")
    else :
        HttpResponse("Invalid Method")

def orders(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            id = request.user.id
            usr_orders = Order.objects.annotate(
                status_display=Case(
                    When(status='MK1', then=Value('Menunggu Pembayaran')),
                    When(status='DP2', then=Value('Sedang Diproses')),
                    When(status='SD3', then=Value('Sedang Dikirim')),
                    When(status='ST4', then=Value('Selesai')),
                    default=Value('Menunggu Konfirmasi'),
                    output_field=CharField()
                )
            ).filter(user=request.user.id)
            return render(request, 'profile/orders.html/', context={"orders" : usr_orders})
        else:
            return HttpResponse("Anda Belum Login")
    else :
        return HttpResponse("Invalid Method")      

def order_detail(request, id):
    if request.method == 'GET':
        if request.user.is_authenticated:            
            get_ordID = Order.objects.annotate(
                status_display=Case(
                    When(status='MK1', then=Value('Menunggu Pembayaran')),
                    When(status='DP2', then=Value('Sedang Diproses')),
                    When(status='SD3', then=Value('Sedang Dikirim')),
                    When(status='ST4', then=Value('Selesai')),
                    default=Value('Menunggu Konfirmasi'),
                    output_field=CharField()
                )
            ).get(pk=id, user=request.user.id)

            if get_ordID:
                products = Cart.objects.filter(order=id)  
            else:
                return HttpResponse("Pesanan tidak ditemukan")
            
            return render(request, 'profile/single-order.html/', context={'order' : get_ordID, 'products' : products})
        else:
            return HttpResponse("Anda belum login / Access Denied")
    else:
        return HttpResponse("Invalid Method")       

def user_address(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            try:
                address = Address.objects.get(user=request.user.id)
            except:
                address=None
            return render(request, 'profile/address.html/', {"context" : address})
        else:
            HttpResponse("Anda Belum Login")
    else :
        HttpResponse("Invalid Method")

def change_address(request):
    if request.method == 'POST':
        form = AddressForm(data=request.POST)
        
        if form.is_valid():
            # address = form.save(commit=False)
            clean_data = form.cleaned_data
            if request.user.is_authenticated:
                clean_data['user'] = request.user                        
            try:
                Address.objects.update_or_create(
                    user=request.user,
                    defaults=clean_data
                )
            except:
                return HttpResponse("Gagal")
            return redirect('/account/')
        print("form error : ", form.errors)
    else:
        init_val = {
            'first_name' : request.user.first_name,
            'last_name'  : request.user.last_name,
            'email' : request.user.email,
        }
        ori_addr = None
        # user = None
        # if request.user.is_authenticated: 
        #     user = request.user.id


        if Address.objects.filter(user=request.user.id).exists():
            ori_addr = Address.objects.get(user=request.user.id)
            init_val['province'] = ori_addr.province
            init_val['city'] = ori_addr.city
            init_val['alamat'] = ori_addr.alamat
            init_val['post_code'] = ori_addr.post_code
            
        form = AddressForm(address=ori_addr)
    return render(request, 'profile/change-address.html', {'form': form})

def download(request):
    pass

def details(request):
    pass