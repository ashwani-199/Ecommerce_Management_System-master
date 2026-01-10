from apps.product.models import Product
from apps.users.models import User
# from apps.shipping_cart.models import Cart

class Carts():
    def __init__(self, request):
        self.session = request.session
        self.request = request

        # Get user the current session key if it exists
        cart = self.session.get('session_key')

        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}


        self.cart = cart

    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = str(quantity)

        if product_id in self.cart:
            pass
        else:
            self.cart[product_id] = int(product_qty)
        
        self.session.modified = True

    
    def cart_total(self):
        product_ids = self.cart.keys()

        products = Product.objects.filter(id__in=product_ids)

        quantity = self.cart

        total = 0

        for key, value in quantity.items():
            key = int(key)
            for product in products:
                if product.id == key:
                    if product.sale_price:
                        total = total + (product.sale_price * value)
                    else:
                        total = total + (product.price * value)

        return total
        


    def __len__(self):
        return len(self.cart)
    

    def get_products(self):

        product_ids = self.cart.keys()

        products = Product.objects.filter(id__in=product_ids)

        return products
    
    def get_one_products(self):
        product_ids = self.cart.keys()
        products = Product.objects.get(id__in=product_ids)
        return products
    
    def get_quants(self):
        quantities = self.cart
        return quantities
    
    def update(self, product, quantity):
        product_id = str(product)
        quantity_id = str(quantity)

        self.cart[product_id] = int(quantity_id)
        self.session.modified = True

        things = self.cart
        return things
    
    def delete(self, product):
        product_id = str(product)

        if product_id in self.cart:
            del self.cart[product_id]

        self.session.modified = True