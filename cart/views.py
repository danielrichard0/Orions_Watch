from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Cart
from products.models import Product
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .cart import CartProcessor
from .forms import TransactionForm, AddressForm
from customers.models import City, District, Villages, ProvinceRajaOngkir, CityRajaOngkir
from orders.models import Order
from django.contrib.sessions.models import Session
from django.db.models import Sum, F, Case,When,Value,CharField
from urllib.parse import urlencode
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from customers.models import Address
from .raja_ongkir import get_city, get_region, get_ongkir

# Create your views here.
def insert_cart(request):
    if request.method == 'POST' and request.session.session_key:
        prod_id = request.POST.get('prod_id')
        quantity = request.POST.get('quantity', 1)
        product = get_object_or_404(Product, pk=prod_id)

        if product.stock < int(quantity):
            return JsonResponse({"error" :"Jumlah yang anda pilih melebihi stok kami"}, status=500)

        if request.user.is_authenticated:
            user_identifier = {'user_id': request.user.id}
        else :
            ses_mod = get_object_or_404(Session, session_key=request.session.session_key)
            user_identifier = {'session' : ses_mod}


        cart_item, created = Cart.objects.get_or_create(product=product, defaults={'quantity':1}, order_id__isnull=True,**user_identifier) 
        if not created:
            if cart_item.quantity + int(quantity) > product.stock:
                return JsonResponse({"error" :"Jumlah yang anda pilih melebihi stok kami"}, status=500)
            cart_item.quantity += int(quantity)
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
    
def hit_ongkir (request):
    if request.method == 'GET':
        cart = CartProcessor(request)   
        weight = cart.total_weight
        origin = 455
        city = request.GET.get('city')

        data = get_ongkir(origin, city, weight, 'jne')
        if data.get("error", False):
            return HttpResponse("Gagal")
        if data['rajaongkir']['status']['code'] == 200 :
            results = data['rajaongkir']['results']
            transaksi_comp = render(request, 'cart/transaksi-pesanan.html', context={"content" : results}).content.decode('utf-8')
            return JsonResponse({"component" : transaksi_comp})
        else :
            return HttpResponse("Gagal")
    
    else :
        HttpResponse("Invalid Response")
    
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
        return render(request, 'cart/select-cart.html', {"title" : "Keranjang"})
    else:
        return HttpResponse("invalid request method")
    
def count_total(request):
    if request.method == 'GET':
        cart = CartProcessor(request)
        ongkir = request.GET.get('ongkir')
        if ongkir:           
            details = ongkir.split('|')
            total_final = cart.total + int(details[0])
            return JsonResponse({"total" : total_final})
        else:
            return HttpResponse("Gagal")

    
def make_order(request):
    results = None
    if request.method == 'POST':
        try :
            ongkir = request.POST.get('radio-pengiriman', None)
        except Exception as e:
            return JsonResponse({"error" : "Gagal ambil data ongkos kirim"}, status=500)
        details_ongkir = ongkir.split('|')
        if not ongkir:
            return HttpResponse("Gagal olah data ongkir")
        
        harga_ongkir = int(details_ongkir[0])
        agen_pengiriman = details_ongkir[1]
        services = details_ongkir[2]



        form = TransactionForm(data=request.POST)
        cart = CartProcessor(request)

        if not cart.cart : 
            return HttpResponse("Keranjang Anda Kosong")
        
        if form.is_valid():
            address = form.save()
            address_id = address.id

            clean_data = form.cleaned_data 
            user = None
            is_guest = False
            
            if request.user.is_authenticated:
                is_guest = False
                user = request.user
            else : 
                is_guest = True

            make_order = Order(
                address_id=address_id,
                is_guest=is_guest,
                cust_note= clean_data.get('cust_note'), 
                first_name=clean_data.get('first_name'), 
                last_name=clean_data.get('last_name'),
                email=clean_data.get('email'),
                total_price=cart.subtotal,
                total_final=cart.subtotal+harga_ongkir,
                user=user,
                status='MK1',
                ongkir=harga_ongkir,
                agen_pengiriman = agen_pengiriman,
                service_pengiriman = services
                )
            
            make_order.save()        
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
                for prod in products:
                    obj = prod.product
                    obj.stock = obj.stock - prod.quantity
                    if not obj.sold :
                        obj.sold = prod.quantity
                    else:
                        obj.sold += prod.quantity
                    obj.save() 

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
        addr=None
        if request.user.is_authenticated:
            try :
                addr = Address.objects.get(user=request.user)
                cart = CartProcessor(request)
                data = get_ongkir(455, addr.city.id, cart.total_weight, 'jne')
                if data['rajaongkir']['status']['code'] == 200 :
                    results = data['rajaongkir']['results']                    
            except:
                addr = None
        form = TransactionForm(address=addr)
    return render(request, 'cart/transaction.html', {"form" : form, "content" : results, "title": "Transaksi"})

def order_details(request):
    ord_id = request.GET.get('q')
    token = request.GET.get('token')

    if not ord_id or not token:
        return HttpResponse("Pesanan tidak ada")

    # harusnya bisa dibawa dari cart
    try :
        order = Order.objects.annotate(
                    status_display=Case(
                        When(status='MK1', then=Value('Menunggu Pembayaran')),
                        When(status='DP2', then=Value('Sedang Diproses')),
                        When(status='SD3', then=Value('Sedang Dikirim')),
                        When(status='ST4', then=Value('Selesai')),
                        default=Value('Menunggu Konfirmasi'),
                        output_field=CharField()
                    )
                ).get(pk=ord_id, token=token)
    except Exception as e:
        return HttpResponse(f"Gagal ambil data order ({e})")
    products = Cart.objects.filter(order=order)
    title = f"Pesanan | {order.id} | {order.status_display}"

    return render(request, 'cart/order-details.html', {'order' : order, 'products' : products, "title" : title})

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
    

def select_city_rajaongkir(request):
    if request.method == "GET":
        prov = request.GET.get('province_id')
        if prov:

            cities = CityRajaOngkir.objects.filter(province_id=prov)
            cities = list(cities.values('id', 'city_name'))
            return JsonResponse({"cities" : cities})
        else:
            return HttpResponse("Gagal")

    else:
        return HttpResponse("invalid request method")


