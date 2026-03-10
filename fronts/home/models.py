from django.db import models
from apps.users.models import User
from apps.product.models import Product, Color, Size



class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart for {self.user.username}"

    # def get_total_price(self):
    #     total = sum(item.get_total_price() for item in self.cartitem_set.all())
    #     return total

    def get_total_price_with_sale(self):
        total = sum(item.get_total_price_with_sale() for item in self.cartitem_set.all())
        return total
    
    def get_total_price(self):
        total = sum(item.get_total_price() for item in self.cartitem_set.all())
        return total

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='cartitem_set', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, null=True, blank=True, on_delete=models.SET_NULL)
    color = models.ForeignKey(Color, null=True, blank=True, on_delete=models.SET_NULL)
    quantity = models.PositiveIntegerField(default=1)

    def get_total_price(self):
        return self.product.price * self.quantity

    def get_total_price_with_sale(self):
        if self.product.is_sale:
            return self.product.sale_price * self.quantity
        return self.get_total_price()

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
