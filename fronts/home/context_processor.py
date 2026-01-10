from fronts.home.models import CartItem

def cart(request):
    cart = CartItem.objects.filter(cart__user=request.user.id)
    
    if cart is None:
        return {'cart_count': None}
    else:
        return {'cart_count': cart.count()}
    