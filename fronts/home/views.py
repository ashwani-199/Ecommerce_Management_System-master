from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from apps.product.models import Product, ProductImage, ProductCategory, ProductReview, Color, Size
from django.http import JsonResponse
from django.db.models import F
from django.utils import timezone
from apps.product.serializers import ProductSerializers
from apps.users.models import User
from apps.payment.models import Payment
from django.contrib.auth.hashers import make_password
from fronts.home.models import Cart, CartItem
from django.contrib.auth.decorators import login_required
from fronts.home.forms import ProfileEditForm, LoginForm, UserAddForm, CheckoutForm
from django.core.mail import send_mail
from django.conf import settings
from apps.orders.models import Order, OrderItem

def register_user(request):
    if request.method == 'POST':
        form = UserAddForm(request.POST or None)
        if form.is_valid():
            users = User()
            users.user_role_id = 3
            users.username = form.cleaned_data["username"]
            users.first_name =form.cleaned_data["first_name"]
            users.last_name = form.cleaned_data["last_name"]
            users.email = form.cleaned_data["email"]
            users.password = make_password(form.cleaned_data["password"])
            users.is_staff = True
            subject = 'Welcome to Registration Account.'
            message = f'Hi {users.username}, Thank you for Registration Account in Acuity Fashion Management System.'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [users.email, ]
            # send_mail( subject, message, email_from, recipient_list )
            users.save()
            messages.success(request, "Your account is registered successfully")
            return redirect("home.login_user")
        
        
        else:
            for field in form.errors:
                form[field].field.widget.attrs['class'] += ' is-invalid'

    else:
        form = UserAddForm()


    context = {
        "form": form,
    }

    return render(request, 'frontends/register.html', context)

def login_user(request):
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

                messages.success(request, "You are now logged in")
                return redirect('home.index')
            else:
                messages.error(request, "Invalid Credentials")
                return redirect("home.login_user")
        else:
            for field in form.errors:
                form[field].field.widget.attrs['class'] += ' is-invalid'

    else:
        form = LoginForm()

    context = {
        "form": form
    }

    return render(request, 'frontends/login.html', context)

def user_logout(request):
    logout(request)
    messages.success(request, "You are now logged out")
    return redirect('home.login_user')


@login_required(login_url='login')
def profile(request):
    userDetail = User.objects.filter(id=request.user.id, is_active=True, is_delete=False).first()
    if not userDetail:
        return redirect('home.profile')
    initialDict = {
        "email": userDetail.email,
        "username": userDetail.username,
        "first_name": userDetail.first_name,
        "last_name": userDetail.last_name,
        "image": userDetail.image,
        "gender":userDetail.gender,        
           
}
    form = ProfileEditForm(initial=initialDict)
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=userDetail)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile has been updated successfully")
            return redirect('home.index')
        
        else:
            for field in form.errors:
                form[field].field.widget.attrs['class'] += ' is-invalid'
        
    context = {
        "form": form,
        "show_image": userDetail.image
    }
    return render(request, "frontends/profile.html", context)


def category(request, foo):
    foo = foo.replace('-',' ')
    
    category = ProductCategory.objects.get(name=foo)
    products = Product.objects.filter(categories=category)

    context = {
        'products': products,
        'category': category,
    }
    return render(request, 'frontends/category.html', context)


def index(request):
    products = Product.objects.all()
        
    product_review = ProductReview.objects.filter(rating=5)
    
    context = {
        "home_page": "active",
        "products": products,
        "product_review": product_review,
    }
    return render(request, 'frontends/index.html', context)


def about(request):
    context = {"about_page": "active"}
    return render(request, 'frontends/about.html', context)



def product(request):
    productObj = Product.objects.all()
    context = {
        'product_results': productObj,
        "product_page": "active"
    }
    return render(request, 'frontends/product.html', context)


def productDetails(request, id):
    productObj = Product.objects.get(id=id)
    product_image = ProductImage.objects.filter(product=productObj)
    product_image1 = Product.objects.all()

    product_review = ProductReview.objects.filter(product=productObj).order_by('-id')
    
    try:
        product_rev = ProductReview.objects.get(id=productObj.id)
    except ProductReview.DoesNotExist:
        product_rev = None

    context = {
        'productObj': productObj,
        'product_image': product_image,
        'product_image1':product_image1,
        'product_review': product_review,
        'product_rev': product_rev,
    }
    return render(request, 'frontends/product-detail1.html', context)



def shopCart(request):
    return render(request, 'frontends/shoping-cart.html')




def product_review(request):
    if request.POST.get('action') == 'post':
        product_id = request.POST.get('product_id')
        name = request.POST.get('name')
        review = request.POST.get('review')
        rating = int(request.POST.get('rating'))

        product = get_object_or_404(Product, id=product_id)

        product_review = ProductReview()
        product_review.product = product
        product_review.user = request.user
        product_review.description = review
        product_review.rating = rating
        product_review.save()

        context = {
            'SUCCESS': 'Save'
        }

        response = JsonResponse(context)
        return response
    




@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_items = CartItem.objects.filter(cart=cart)
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
    }
    return render(request, 'frontends/cart_details.html', context)

@login_required
def add_to_cart(request, product_id):
    """Add a product to the user's cart.

    This view supports a POST form that can include optional size/color and quantity.
    If accessed via GET, it redirects back to the product detail page.
    """

    product = get_object_or_404(Product, id=product_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)

    try:
        quantity = max(1, int(request.POST.get('quantity', 1)))
    except (TypeError, ValueError):
        quantity = 1

    size = None
    color = None

    size_id = request.POST.get('size')
    color_id = request.POST.get('color')
    if size_id:
        size = get_object_or_404(Size, id=size_id)
    if color_id:
        color = get_object_or_404(Color, id=color_id)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        size=size,
        color=color,
        defaults={'quantity': quantity},
    )

    if not created:
        cart_item.quantity = F('quantity') + quantity
        cart_item.save()
        cart_item.refresh_from_db()

    return redirect('cart_detail')

@login_required
def remove_from_cart(request, product_id):
    cart = Cart.objects.get(user=request.user)
    cart_item = CartItem.objects.get(cart=cart, product__id=product_id)
    cart_item.delete()
    return redirect('cart_detail')

@login_required
def update_cart_item(request, product_id):
    if request.method == 'POST':
        new_quantity = int(request.POST.get('quantity'))
        cart = Cart.objects.get(user=request.user)
        cart_item = CartItem.objects.get(cart=cart, product__id=product_id)

        if new_quantity > 0:
            cart_item.quantity = new_quantity
            cart_item.save()
        else:
            cart_item.delete()

    return redirect('cart_detail')



@login_required
def checkout(request):
    cart = Cart.objects.get(user=request.user)

    # Use the sale-aware total if the cart has any sale-priced items.
    total_price = cart.get_total_price_with_sale()

    cart_items = CartItem.objects.filter(cart=cart)
    
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Create Order
            order = Order.objects.create(
                customer=request.user,
                shipping_address=form.cleaned_data['shipping_address'],
                total_amount=total_price,
                status='Pending'
            )
            
            # Create OrderItems from CartItems (respect sale price)
            for item in cart_items:
                unit_price = item.product.sale_price if item.product.is_sale else item.product.price
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=unit_price,
                    total_price=item.get_total_price_with_sale()
                )
            
            # Create a payment record
            payment_method = form.cleaned_data.get('payment_method')
            payment_status = 'Completed' if payment_method == 'Online' else 'Pending'
            Payment.objects.create(
                order=order,
                customer=request.user,
                amount=total_price,
                payment_date=timezone.localdate(),
                payment_method=payment_method,
                status=payment_status,
            )

            # Clear the cart
            cart_items.delete()
            return redirect('order_confirmation', order_id=order.id)
        else:
            for field in form.errors:
                form[field].field.widget.attrs['class'] += ' is-invalid'
        
    else:
        form = CheckoutForm()
    
    return render(request, 'frontends/checkout.html', {'form': form, 'cart_items': cart_items, 'total_price': total_price})

def order_confirmation(request, order_id):
    order = Order.objects.get(id=order_id)
    order_items = OrderItem.objects.filter(order=order)
    payment = Payment.objects.filter(order=order).first()
    return render(request, 'frontends/order_confirmation.html', {
        'order': order,
        'order_items': order_items,
        'payment': payment,
    })