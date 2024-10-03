from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Cart
from products.models import Product
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .cart import CartProcessor
from .forms import TransactionForm, AddressForm
from customers.models import City, District, Villages
from orders.models import Order
from django.contrib.sessions.models import Session
from django.db.models import Sum, F
from urllib.parse import urlencode
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from customers.models import Address

# Create your views here.
def insert_cart(request):
    if request.method == 'POST' and request.session.session_key:
        prod_id = request.POST.get('prod_id')
        product = get_object_or_404(Product, pk=prod_id)

        if request.user.is_authenticated:
            user_identifier = {'user_id': request.user.id}
        else :
            ses_mod = get_object_or_404(Session, session_key=request.session.session_key)
            user_identifier = {'session' : ses_mod}


        cart_item, created = Cart.objects.get_or_create(product=product, defaults={'quantity':1}, order_id__isnull=True,**user_identifier) 
        if not created:
            cart_item.quantity += 1
            cart_item.save()

        return HttpResponse("Data telah dimasukan ke keranjang")
    else:
        return HttpResponse("Invalid request method")
    
def get_cart_component(request):
    if request.method == 'GET':
        return render(request, 'cart/cart-component.html')
    else:
        return HttpResponse("Invalid request method")
    
def update_cart_overall(request):
    if request.method == 'GET':
        side_cart = render(request, 'cart/cart-component.html').content.decode('utf-8')
        table_items = render(request, 'cart/table-items-component.html').content.decode('utf-8')
        table_totals = render(request, 'cart/table-totals-component.html').content.decode('utf-8')

        return JsonResponse({
            'side_cart' : side_cart,
            'table_items' : table_items,
            'table_totals' : table_totals 
        })

    else:
        return HttpResponse("Invalid request method")
    
def get_quantity(request):
    if request.method == 'GET':
        cart = CartProcessor(request)
        q = cart.quantity
        return JsonResponse({"q" : q})
    else:
        return HttpResponse("Invalid request method")
    
def change_quantity(request):
    if request.method == 'POST':
        item_id = request.POST.get('id')
        new_q = request.POST.get('new_q')

        their_item = Cart.objects.get(pk=item_id)

        if int(new_q) < 1:
            their_item.delete()
        else :
            their_item.quantity = new_q
            their_item.save()
        
        return HttpResponse("Keranjang diperbarui")
    else:
        return HttpResponse("Invalid request method")

    
def delete_item(request):
    if request.method == 'POST' and request.session.session_key:
        prod_id = request.POST.get('prod_id')
        render_all = request.POST.get('rndr_all')

        if request.user.is_authenticated:
            identifier = {"user_id" : request.user.id}
        else :
            identifier = {"session_id" : request.session.session_key}
        identifier['id'] = prod_id

        # product = Product.objects.get(pk=prod_id)
        cart = Cart.objects.get(**identifier)
        cart.delete()

        # side cart, item dan total, 3 component harus diperbarui sehabis delete 
        if render_all:
            side_cart = render(request, 'cart/cart-component.html').content.decode('utf-8')
            table_items = render(request, 'cart/table-items-component.html').content.decode('utf-8')
            table_totals = render(request, 'cart/table-totals-component.html').content.decode('utf-8')

            return JsonResponse({
                'side_cart' : side_cart,
                'table_items' : table_items,
                'table_totals' : table_totals 
            })

        return HttpResponse("data berhasil di hapus")
    else:
        return HttpResponse("Invalid request method")
    
def select_cart(request):
    if request.method == 'GET':
        return render(request, 'cart/select-cart.html')
    else:
        return HttpResponse("invalid request method")
    
def make_order(request):
    if request.method == 'POST':
        form = TransactionForm(data=request.POST)
        cart = CartProcessor(request)

        if form.is_valid():
            address = form.save()
            address_id = address.id

            clean_data = form.cleaned_data 
            cust_note = clean_data.get('cust_note')
            first_n = clean_data.get('first_name')
            last_n = clean_data.get('last_name')
            email = clean_data.get('email')
            is_save = clean_data.get('is_save')
            user = None
            
            if request.user.is_authenticated:
                user = User.objects.get(pk=request.user.id)

            make_order = Order(
                address_id=address_id,
                is_guest=False,
                cust_note=cust_note, 
                first_name=first_n, 
                last_name=last_n,
                email=email,
                total_price=cart.subtotal,
                total=cart.total,
                user=user,
                status='MK1',
                ongkir=20000
                )
            
            make_order.save()        
            print("make order : ", make_order)
            commit_ord = cart.commit_order(make_order.id)
            
            if(commit_ord['status']):
                if request.user.is_authenticated : 
                    address_dt = clean_data
                    del address_dt['cust_note']
                    del address_dt['is_save']
                    try:
                        Address.objects.update_or_create(
                            user=request.user,
                            defaults=address_dt
                        )
                    except:
                        return HttpResponse("Gagal Banget")

                ord_id = int(make_order.id) 
                ord_key = make_order.token
                products = Cart.objects.filter(order=ord_id)

                context = {'order' : make_order}
                txt_content = render_to_string(
                    'cart/text-email.txt',
                    context
                )

                html_content = render_to_string(
                    'cart/email-template.html',
                    context = {'order' : make_order, 'products' : products, 'address' : address }
                )

                msg = EmailMultiAlternatives(
                    "Pesanan Anda Telah Kami Terima",
                    txt_content,
                    "admin@fetishia.store",
                    [make_order.email],
                )

                
                msg.attach_alternative(html_content, "text/html")
                msg.send()
                            
                query_param = {"q" : ord_id, "token" : ord_key}
                base_url = reverse('cart:checkout-order')
                full_url = f"{base_url}?{urlencode(query_param)}"
                
                return redirect(full_url)
            else:
                return HttpResponse("Gagal")
        else:
            print("the form : ", form.errors)
    else:
        addr=None
        if request.user.is_authenticated:
            try :
                addr = Address.objects.get(user=request.user)
            except:
                addr = None
        form = TransactionForm(address=addr)
    return render(request, 'cart/transaction.html', {"form" : form})

def order_details(request):
    ord_id = request.GET.get('q')
    token = request.GET.get('token')

    if not ord_id or not token:
        return HttpResponse("Pesanan tidak ada")

    # harusnya bisa dibawa dari cart
    order = get_object_or_404(Order, pk=ord_id, token=token)
    products = Cart.objects.filter(order=order)
    subtotal = products.aggregate(total=Sum(F('product__price') * F('quantity')))['total']
    return render(request, 'cart/order-details.html', {'order' : order, 'products' : products, 'subtotal' : subtotal})

def select_city(request):

    if request.method == "GET":
        prov = request.GET.get('province_id')
        if prov:
            cities = City.objects.filter(province_id=prov)
            cities = list(cities.values('id', 'name'))
            return JsonResponse({"cities" : cities})
        else:
            return HttpResponse("Gagal")

    else:
        return HttpResponse("invalid request method")
    
def select_district(request):
    if request.method == "GET":
        city = request.GET.get('city_id')
        if city:
            districts = District.objects.filter(city_id=city)
            districts = list(districts.values('id', 'name'))
            return JsonResponse({"districts" : districts})
        else:
            return HttpResponse("Gagal")

    else:
        return HttpResponse("invalid request method")
    
def select_village(request):
    if request.method == "GET":
        district = request.GET.get('district_id')
        if district:
            villages = Villages.objects.filter(district_id=district)
            villages = list(villages.values('id', 'name'))
            return JsonResponse({"villages" : villages})
        else:
            return HttpResponse("Gagal")

    else:
        return HttpResponse("invalid request method")
    


