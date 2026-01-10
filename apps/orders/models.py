from django.db import models
from apps.product.models import Product
from apps.users.models import User

 
STATUS =(
        ('Pending','Pending'),
        ('Order Confirmed','Order Confirmed'),
        ('Out for Delivery','Out for Delivery'),
        ('Delivered','Delivered'),
    )

class Order(models.Model):
    order_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=100, decimal_places=3)
    status = models.CharField(max_length=50,null=True,choices=STATUS)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    shipping_address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Total amount #{self.total_amount} for order #{self.id}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=100, decimal_places=3, blank=True, null=True)
    total_price = models.DecimalField(max_digits=100, decimal_places=3)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Total amount#{self.total_price} for order #{self.id}"

class OrderHistory(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    status = models.CharField(max_length=50,null=True,choices=STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.status
    