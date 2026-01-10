from django.db import models
from apps.orders.models import Order
from apps.users.models import User

STATUS =(
        ('Cash','Cash'),
        ('Online','Online'),
    )
class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    payment_method = models.CharField(max_length=50,null=True,choices=STATUS)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment #{self.id} by {self.order.customer.username}"
    