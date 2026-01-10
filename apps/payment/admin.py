from django.contrib import admin
from . models import ClientPayment, OrderPayment, Invoice, Transaction, Payment, PaymentMethod
# Register your models here.


admin.site.register(ClientPayment)
admin.site.register(OrderPayment)
admin.site.register(Invoice)
admin.site.register(Transaction)
admin.site.register(Payment)
admin.site.register(PaymentMethod)