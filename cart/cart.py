from django.db.models import Sum, F
from .models import Cart


class CartProcessor():
    def __init__(self, request):
        self.cart = None
        self.subtotal = 0
        self.quantity = 0
        self.total = 0
        identifier = {}

        if not request.session.session_key:
            request.session.save()
        if request.user.is_authenticated:
            identifier = {"user_id" : request.user.id} 
        elif request.session.session_key:
            identifier =  {"session_id" : request.session.session_key}

        self.cart = Cart.objects.filter(**identifier, order_id__isnull=True)
        if self.cart.exists():
            self.subtotal = self.cart.aggregate(total=Sum(F('product__price') * F('quantity')))['total']
            self.total = self.subtotal + 20000
            self.quantity = self.cart.all().count()

    # setelah commit order, otomatis class ini hilang
    def commit_order(self, order_id):
        if self.cart :
            self.cart.update(order=order_id) 
            return {"status":True}
        else:
            return {"status": False}
        
    # def subtotal(self, order_id):
    #     if self.cart : 
    #         products = Cart.objects.filter(order=order_id)
    #         subtotal = products.aggregate(total=Sum(F('product__price') * F('quantity')))['total']
    #         return subtotal