from .cart import CartProcessor

def cart(request):    
    return {'cart' : CartProcessor(request)}