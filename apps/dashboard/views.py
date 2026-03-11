from django.shortcuts import render
from apps.users.models import User
from apps.product.models import Product
from apps.orders.models import Order
from django.core.paginator import Paginator

# Create your views here.
def index(request):
    users_obj = User.objects.filter(is_active=True).order_by('-id')
    admin = User.objects.filter(user_role_id=1, is_active=True).count()
    staff = User.objects.filter(user_role_id=2, is_active=True).count()
    customers = User.objects.filter(user_role_id=3, is_active=True).count()
    product = Product.objects.filter().count()
    orders = Order.objects.filter().count()

    totalRecord = users_obj.count()
    paginator = Paginator(users_obj, 4)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'admin': admin,
        'merchants': staff,
        'customers':customers,
        'vendors': product,
        'orders': orders,
        'users_obj':users_obj,
        'totalRecord': totalRecord,
    }
    return render(request, 'dashboard/index.html', context)

