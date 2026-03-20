from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from apps.product.models import Product, ProductCategory, ProductImage, ProductReview
from apps.product.forms import ProductForm, CategoryForm, ImageForm, ProductEditForm
from django.contrib import messages
from django.forms import modelformset_factory
from mysite_management.common_module.validationMessage import Messages


SINGULAR_NAME = "Product"
PLURAL_NAME = "Products"

@login_required(login_url='login')
def index(request):
    DB = Product.objects.filter().order_by('-id')
    
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
    return render(request, 'product/index.html', context)

@login_required(login_url='login')
def addProduct(request):
    ImageFormSet = modelformset_factory(ProductImage, form=ImageForm, extra=3)
    if request.method == 'POST':
        productForm = ProductForm(request.POST, request.FILES)
        formset = ImageFormSet(request.POST,  request.FILES, queryset=ProductImage.objects.none())

        if productForm.is_valid() and formset.is_valid():
            post_form = productForm.save(commit=False)
            post_form.user = request.user
            post_form.save()

            for form in formset.cleaned_data:
                
                if form:
                    image = form['image']
                    photo = ProductImage(product=post_form, image=image)
                    photo.save()
            # use django messages framework
            messages.success(request, Messages.PRODUCT_IS_ADD_SUCCESSFULLY.value)
            return redirect("product.index")
        else:
            print(productForm.errors, formset.errors, "Hello ")

    else:
        productForm = ProductForm()
        formset = ImageFormSet(queryset=ProductImage.objects.none())
    context = {
        "form": productForm,
        'formset':formset,
        'singular_name': SINGULAR_NAME,
        'plural_name': PLURAL_NAME,
    }
    return render(request, 'product/add.html', context)

@login_required(login_url='login')
def edit(request, id):
    product = Product.objects.get(id=id)
    product_image = ProductImage.objects.filter(product=product)
    if not product:
        return redirect('product.index')
    initialDict = {
        "name": product.name,
        "description": product.description,
        "price": product.price,
        "brand_name": product.brand_name,
        "categories": product.categories,
        'image': product.image,
        "is_sale": product.is_sale,
        "sale_price": product.sale_price,
    }
    form = ProductEditForm(initial=initialDict)
    if request.method == "POST":
        # include request.FILES so image fields update and we can read uploaded files
        form = ProductEditForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()

            # Handle deletion of selected additional images
            delete_ids = request.POST.getlist('delete_images')
            if delete_ids:
                imgs_to_delete = ProductImage.objects.filter(id__in=delete_ids, product=product)
                for img in imgs_to_delete:
                    try:
                        img.image.delete(save=False)
                    except Exception:
                        pass
                    img.delete()

            # Handle new uploaded images (multiple)
            new_images = request.FILES.getlist('images')
            for uploaded in new_images:
                if uploaded:
                    ProductImage.objects.create(product=product, image=uploaded)

            messages.success(request, Messages.PRODUCT_IS_UPDATED_SUCCESSFULLY.value)
            return redirect('product.index')

    context = {
        'form': form,
        'product_data': product,
        'product_image':product_image,
        'singular_name': SINGULAR_NAME,
        'plural_name': PLURAL_NAME,
    }
    return render(request, 'product/edit.html', context)


@login_required(login_url='login')
def view(request, id):
    product = Product.objects.get(id=id)
    product_image = ProductImage.objects.filter(product=product)

    if not product:
        return redirect('product.index')

    context = {
        'product_data': product,
        'product_image':product_image,
        'singular_name': SINGULAR_NAME,
        'plural_name': PLURAL_NAME,
    }

    return render(request, 'product/view.html', context)


@login_required(login_url='login')
def delete(request, id):
    product = Product.objects.get(id=id)
    if not product:
        return redirect('product.index')
    product.delete()
    messages.success(request, Messages.PRODUCT_IS_DELETED_SUCCESSFULLY.value)
    return redirect('product.index')



@login_required(login_url='login')
def addCategory(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST or None)
        if form.is_valid():
            product_category = ProductCategory()
            product_category.name = form.cleaned_data["name"]
            product_category.save()
            messages.success(request, Messages.CATEGORY_IS_ADD_SUCCESSFULLY.value)
            return redirect("product.index")

    else:
        form = CategoryForm()
    context = {
        "form": form,
        'singular_name': 'Category',
        'plural_name': 'Categories',
    }
    return render(request, 'product/category.html', context)