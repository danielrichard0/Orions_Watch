from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.shortcuts import render
from django.core.paginator import Paginator
from products.models import Product

def index(request):
    all_product = Product.objects.all()[:8]
    print("test : ", type(all_product[1].price))
    return render(request, "index.html", {"products" : all_product})