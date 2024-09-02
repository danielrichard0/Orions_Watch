from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from products.models import Product, Category
from django.conf import settings

class IndexView(generic.ListView):
    template_name = "products/index.html"
    context_object_name = "all_products"

    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            return Product.objects.filter(category__slug=category_slug)
        else :
            return Product.objects.order_by('date_created')[:8]
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()  
        return context
    
class CategoryView(generic.ListView):
    template_name = "products/index.html"
    context_object_name = "categorized_prods"

    def get_queryset(self):
        return Product.objects.get()