from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import authenticate 
from django.contrib.auth import login 
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.shortcuts import redirect, render
from .form import LoginForm, ProfileEditForm, ForgotPasswordForm, PasswordRestForm
from apps.users.models import User
from apps.login.form import RegisterForm
from mysite_management.common_module.mainService import MainService
from mysite_management.common_module.validationMessage import Messages
from django.core.mail import send_mail
from django.conf import settings


# Create your views here.
def user_login(request):
    if request.method == "GET":
        nextUrl = request.GET.get('next', None)
        request.session['next_url'] = nextUrl

    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)

                messages.success(request, Messages.YOU_ARE_NOW_LOGGED_IN.value)
                return redirect('index')
            else:
                messages.error(request, Messages.INVALID_CREDENTIALS.value)
                return redirect("login")
        else:
            for field in form.errors:
                form[field].field.widget.attrs['class'] += ' is-invalid'

    else:
        form = LoginForm()
    context = {
        "form": form
    }
    return render(request, "login/login.html", context)



def user_register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST or None)
        if form.is_valid():
            users = User()
            users.user_role_id = 2
            users.username = form.cleaned_data["username"]
            users.first_name =form.cleaned_data["first_name"]
            users.last_name = form.cleaned_data["last_name"]
            users.email = form.cleaned_data["email"]
            users.password = make_password(form.cleaned_data["password"])
            users.is_staff = True
            # subject = 'Welcome to Registration Account.'
            # message = f'Hi {users.username}, Thank you for Registration Account in Acuity Fashion Management System.'
            # email_from = settings.EMAIL_HOST_USER
            # recipient_list = [users.email, ]
            # send_mail( subject, message, email_from, recipient_list )
            users.save()
            messages.success(request, Messages.YOUR_ACCOUNT_IS_REGISTRATED_SUCCESSFULLY.value)
            return redirect("login")
        
        
        else:
            for field in form.errors:
                form[field].field.widget.attrs['class'] += ' is-invalid'

    else:
        form = RegisterForm()
    context = {
        "form": form,
    }
    return render(request, "login/register.html", context)



def user_logout(request):
    logout(request)
    messages.success(request, Messages.LOGOUT_USER.value)
    return redirect('login')


@login_required(login_url='login')
def profile(request):
    userDetail = User.objects.filter(id=request.user.id, is_active=True, is_delete=False).first()
    if not userDetail:
        return redirect('index')
    initialDict = {
        "email": userDetail.email,
        "first_name": userDetail.first_name,
        "last_name": userDetail.last_name,
    }
    form = ProfileEditForm(initial=initialDict)
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=userDetail)
        if form.is_valid():
            form.save()
            messages.success(request, Messages.PROFILE_IS_UPDATED_SUCCESSFULLY.value)
            return redirect('index')
        
        else:
            for field in form.errors:
                form[field].field.widget.attrs['class'] += ' is-invalid'
        
    context = {
        "form": form
    }
    return render(request, "login/profile.html", context)

def forgotPassword(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            users = User.objects.filter(email=email)
            if len(users) > 0:
                user = users.first()
                # Create password forgot url and save in db
                service = MainService(request)
                user = service.passwordForgotLink(user)
                tokenString = user.forgot_password_string
                forgotPasswordUrl = service.createUrlString(tokenString)
                subject = 'Welcome to Reset Password Link'
                message = f'Hi {user.username}, Thank you for request a reset password link - {forgotPasswordUrl} in Mysite Management System.'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [user.email, ]
                send_mail( subject, message, email_from, recipient_list )
                return redirect('login')

        else:
            for field in form.errors:
                form[field].field.widget.attrs['class'] += ' is-invalid'
                        
    else:
        form = ForgotPasswordForm()
    context = {
        "form": form
    }
    return render(request, 'login/forgot.html', context)


def passwordReset(request, token):
    userObj = User.objects.filter(forgot_password_string=token).first()
    if not userObj:
        return redirect('login')
    form = PasswordRestForm()
    if request.method == "POST":
        form = PasswordRestForm(request.POST, userObj)
        if form.is_valid():
            password = make_password(form.cleaned_data.get("confirm_password"))
            userObj.password = password
            userObj.confirm_password = form.cleaned_data.get("confirm_password")
            userObj.forgot_password_string = None
            userObj.save()
            return redirect('login')
        
        else:
            for field in form.errors:
                form[field].field.widget.attrs['class'] += ' is-invalid'

    context = {
        "form": form,
        "user_detail": userObj,
        "token": token
    }
    return render(request, 'login/reset_password.html', context)