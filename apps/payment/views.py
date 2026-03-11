from django.shortcuts import render

# Create your views here.
def payment_list(request):
    # This view would list all payments
    return render(request, 'payment/payment_list.html')