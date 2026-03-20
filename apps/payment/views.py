from django.shortcuts import render
from django.core.paginator import Paginator
from apps.payment.models import Payment



SINGULAR_NAME = "Payment"
PLURAL_NAME = "Payments"

# Create your views here.
def payment_list(request):
    DB = Payment.objects.all().order_by('-id')
    
    totalRecord = DB.count()
    paginator = Paginator(DB, 10)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj':page_obj,
        'totalRecord': totalRecord,
        'users_obj': DB,
        'singular_name': SINGULAR_NAME,
        'plural_name': PLURAL_NAME,
    }
    # This view would list all payments
    return render(request, 'payment/index.html', context)