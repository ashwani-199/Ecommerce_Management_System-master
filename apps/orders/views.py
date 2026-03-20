from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from apps.orders.models import Order, OrderItem, OrderHistory
from apps.orders.form import OrderForm
from django.contrib import messages


SINGULAR_NAME = "Order"
PLURAL_NAME = "Orders"

# @login_required(login_url='login')
def index(request):
    DB = Order.objects.all().order_by('-id')
    
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
    return render(request, 'orders/index.html', context)

@login_required(login_url='login')
def edit(request, id):
    order = Order.objects.get(id=id)
    if not order:
        return redirect('orders.index')
    initialDict = {
        "customer" : order.customer,
        "total_amount" : order.total_amount,
        "status": order.status,
        "shipping_address": order.shipping_address

    }
    form = OrderForm(initial=initialDict)
    if request.method == "POST":
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, "Order has been updated successfully.")
            return redirect('orders.index')
    context = {
        'form': form,
        'order': order,
        'singular_name': SINGULAR_NAME,
        'plural_name': PLURAL_NAME,
    }
    return render(request, 'orders/edit.html', context)



@login_required(login_url='login')
def view(request, id):
    order = Order.objects.get(id=id)
    if not order:
        return redirect('orders.index')
    context = {
        'order': order,
        'singular_name': SINGULAR_NAME,
        'plural_name': PLURAL_NAME,
    }
    return render(request, 'orders/view.html', context)


@login_required(login_url='login')
def delete(request, id):
    order = Order.objects.get(id=id)
    if not order:
        return redirect('orders.index')
    order.delete()
    messages.success(request, "Order has been deleted successfully.")
    return redirect('orders.index')



@login_required(login_url='login')
def order_item_index(request):
    DB = OrderItem.objects.filter().order_by('-id')
    
    totalRecord = DB.count()
    paginator = Paginator(DB, 10)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj':page_obj,
        'totalRecord': totalRecord,
        'users_obj': DB,
        'singular_name': "Order Item",
        'plural_name': "Order Items",
    }
    return render(request, 'orderItem/index.html', context)

@login_required(login_url='login')
def order_item_view(request, id):
    order = OrderItem.objects.get(id=id)
    if not order:
        return redirect('orders.index')
    context = {
        'order': order,
        'singular_name': SINGULAR_NAME,
        'plural_name': PLURAL_NAME,
    }
    return render(request, 'orderItem/view.html', context)



@login_required(login_url='login')
def orderItem_delete(request, id):
    order = OrderItem.objects.get(id=id)
    if not order:
        return redirect('order_item.index')
    order.delete()
    messages.success(request, "Order has been deleted successfully.")
    return redirect('order_item.index')