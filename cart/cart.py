from django.db.models import Sum, F
from .models import Cart


class CartProcessor():
    def __init__(self, request):
        self.cart = None
        self.subtotal = 0
        self.quantity = 0
        identifier = {}

        if not request.session.session_key:
            request.session.save()
        if request.user.is_authenticated:
            identifier = {"user_id" : request.user.id} 
        elif request.session.session_key:
            identifier =  {"session_id" : request.session.session_key}

        self.cart = Cart.objects.filter(**identifier)
        if self.cart.exists():
            self.subtotal = self.cart.aggregate(total=Sum(F('product__price') * F('quantity')))['total']
            self.quantity = self.cart.all().count()
