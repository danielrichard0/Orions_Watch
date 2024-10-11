from typing import Any
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from products.models import Product, Category
from django.conf import settings

class IndexView(generic.ListView):
    template_name = "products/index.html"
    context_object_name = "all_products"
    paginate_by = 8

    def get(self, request, *args, **kwargs):
        info = self.request.user.is_authenticated
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        # tidak mungkin query dan category_slug bersamaan (2-2 nya true)
        query = self.request.GET.get('q')
        category_slug = self.kwargs.get('category_slug')
        queryset = Product.objects.order_by('date_created')

        if query:
            queryset = queryset.filter(title__icontains=query)

        elif category_slug:
            queryset = queryset.filter(category__slug=category_slug)
                    
        return queryset[:8]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()  
        context['title'] = "Beranda | Product"
        return context
    
class ProductDetailView(generic.DetailView):
    model = Product
    template_name = 'products/item.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Produk"
        return context

    
class CategoryView(generic.ListView):
    template_name = "products/index.html"
    context_object_name = "categorized_prods"

    def get_queryset(self):
        return Product.objects.get()