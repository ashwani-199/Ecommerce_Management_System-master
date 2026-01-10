from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from apps.users.models import User
from .forms import UserAddForm, UserEditForm
from django.contrib import messages
from mysite_management.common_module.validationMessage import Messages


SINGULAR_NAME = "Staff"
PLURAL_NAME = "Staffs"

@login_required(login_url='login')
def index(request):
    DB = User.objects.filter(user_role_id=2).order_by('-id')
    totalRecord = DB.count()
    paginator = Paginator(DB, 5)  # Show 4 users per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj':page_obj,
        'totalRecord': totalRecord,
        'users_obj': DB,
        'singular_name': SINGULAR_NAME,
        'plural_name': PLURAL_NAME,
    }
    return render(request, 'users/index.html', context)

@login_required(login_url='login')
def add(request):
    if request.method == 'POST':
        form = UserAddForm(request.POST, request.FILES)
        if form.is_valid():
            users = User()
            users.user_role_id = 2
            users.username = form.cleaned_data["username"]
            users.first_name =form.cleaned_data["first_name"]
            users.last_name = form.cleaned_data["last_name"]
            users.email = form.cleaned_data["email"]
            users.mobile_number = form.cleaned_data["mobile_number"]
            users.image = form.cleaned_data["image"]
            users.password = make_password(form.cleaned_data["password"])
            users.confirm_password = make_password(form.cleaned_data["confirm_password"])
            users.is_staff = True
            users.save()
            messages.success(request, Messages.USER_IS_REGISTER.value)
            return redirect("staff.users")
        
        else:
            for field in form.errors:
                form[field].field.widget.attrs['class'] += ' is-invalid'

    else:
        form = UserAddForm()
    context = {
        "form": form,
        'singular_name': SINGULAR_NAME,
        'plural_name': PLURAL_NAME,
    }
    return render(request, 'users/add.html', context)

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
            messages.success(request, Messages.USER_IS_UPDATED_SUCCESSFULLY.value)
            return redirect('staff.users')
        
        else:
            for field in form.errors:
                form[field].field.widget.attrs['class'] += ' is-invalid'

    context = {
        'form': form,
        'user_data': user,
        'singular_name': SINGULAR_NAME,
        'plural_name': PLURAL_NAME,
    }
    return render(request, 'users/edit.html', context)


@login_required(login_url='login')
def view(request, id):
    user = User.objects.get(id=id)
    if not user:
        return redirect('staff.users')

    context = {
        'user_data': user,
    }

    return render(request, 'users/view.html', context)



@login_required(login_url='login')
def delete(request, id):
    user = User.objects.get(id=id)
    print(user.id)
    if not user:
        return redirect('staff.users')
    user.is_delete = True
    user.is_active = False
    messages.success(request, Messages.USER_IS_DELETED_SUCCESSFULLY.value)
    user.save()
    return redirect('staff.users')
