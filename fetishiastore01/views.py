from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.shortcuts import render
from django.core.paginator import Paginator
from products.models import Product
from django.conf import settings


def index(request):
    all_product = Product.objects.filter(image__isnull=False)[:8]
    return render(request, "index.html", {"products" : all_product})

