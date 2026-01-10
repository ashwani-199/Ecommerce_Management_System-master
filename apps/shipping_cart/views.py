from django.shortcuts import render, get_object_or_404
from apps.shipping_cart.cart import Carts
from django.http import JsonResponse
from apps.product.models import Product


# Create your views here.
def cart_index(request):
    cart = Carts(request)
    cart_products = cart.get_products
    quantities = cart.get_quants
    total_price = cart.cart_total

    context = {
        'cart_products': cart_products,
        'quantities':quantities,
        'total_price': total_price
    }

    return render(request, 'frontends/shoping-cart.html', context)



def cart_add(request):

    cart = Carts(request)

    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        quantity_id = int(request.POST.get('quantity_id'))


        productObj = get_object_or_404(Product, id=product_id)

        # Save to session 
        cart.add(product=productObj, quantity=quantity_id)

        # Get Cart Quantity
        cart_quantity = cart.__len__()

        response = JsonResponse({'qty': cart_quantity})
        return response

def update_cart(request):
    cart = Carts(request)

    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        quantity_id = int(request.POST.get('quantity_id'))

        cart.update(product=product_id, quantity=quantity_id)

        response = JsonResponse({'qty': quantity_id})
        return response
    


def delete_cart(request):
    cart = Carts(request)

    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        
        cart.delete(product=product_id)

        response = JsonResponse({'qty': '0'})
        return response