from django.shortcuts import render, redirect
from django.contrib import messages
from apps.users.models import User
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from apps.users.forms import UserEditForm



SINGULAR_NAME = "Customer"
PLURAL_NAME = "Customers"

@login_required(login_url='login')
def index(request):
    DB = User.objects.filter(user_role_id=3)

    totalRecord = DB.count()
    paginator = Paginator(DB, 2)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj':page_obj,
        'totalRecord': totalRecord,
        'users_obj': DB,
        'singular_name': SINGULAR_NAME,
        'plural_name': PLURAL_NAME,
    }
    return render(request, 'customers/index.html', context)


@login_required(login_url='login')
def edit(request, id):
    user = User.objects.get(id=id)
    
    if not user:
        return redirect('index')
    initialDict = {
        "email": user.email,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "mobile_number": user.mobile_number,
        "is_active": user.is_active,
        "image": user.image,   
    }
    form = UserEditForm(initial=initialDict)
    if request.method == "POST":
        form = UserEditForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, f'{SINGULAR_NAME} updated successfully.')
            return redirect('customer.index')
        
        else:
            for field in form.errors:
                form[field].field.widget.attrs['class'] += ' is-invalid'

    context = {
        'form': form,
        'user_data': user,
        'singular_name': SINGULAR_NAME,
        'plural_name': PLURAL_NAME,
    }
    return render(request, 'customers/edit.html', context)


@login_required(login_url='login')
def view(request, id):
    customers = User.objects.get(id=id)
    if not customers:
        return redirect('customer.index')

    context = {
        'customer_data': customers,
    }
    return render(request, 'customers/view.html', context)



@login_required(login_url='login')
def delete(request, id):
    customers = User.objects.get(id=id)
    if not customers:
        return redirect('customer.index')
    customers.is_delete = True
    customers.is_active = False
    messages.success(request, f'{SINGULAR_NAME} deleted successfully.')
    customers.save()
    return redirect('customer.index')