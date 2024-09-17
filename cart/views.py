from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Cart
from products.models import Product
from django.shortcuts import render, get_object_or_404
from .cart import CartProcessor

# Create your views here.
def insert_cart(request):
    if request.method == 'POST' and request.session.session_key:
        prod_id = request.POST.get('prod_id')
        product = get_object_or_404(Product, pk=prod_id)

        if request.user.is_authenticated:
            user_identifier = {'user_id': request.user.id}
        else :
            user_identifier = {'session_id': request.session.session_key}

        cart_item, created = Cart.objects.get_or_create(product=product, defaults={'quantity':1}, **user_identifier) 
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

        if render_all:
            print("executed")
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
    
def transaction(request):
    if request.method == 'GET':
        pass

