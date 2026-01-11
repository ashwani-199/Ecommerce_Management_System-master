from django.db import models
from apps.users.models import User
from django.db.models import Avg



class ProductCategory(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Size(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    brand_name = models.CharField(max_length=255)
    price = models.DecimalField(default=0, decimal_places=2, max_digits=6)
    stock = models.BooleanField(default=True)
    image = models.ImageField(upload_to='product_oneimages/')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    categories = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    is_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(default=0, decimal_places=2, max_digits=6)

    # Additional info
    weight = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    dimensions = models.CharField(max_length=100)
    materials = models.CharField(max_length=255)

    # Many-to-Many relationships
    colors = models.ManyToManyField(Color, related_name="products")
    sizes = models.ManyToManyField(Size, related_name="products")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name



    @property 
    def discount_price(self): 
        """ Returns the sale price if product is on sale, 
        otherwise returns the original price. """ 
        if self.is_sale and self.sale_price > 0: 
            return self.sale_price 
        return self.price 
    
    @property 
    def discount_percent(self): 
        """ Returns the discount percentage if product is on sale, otherwise returns 0. """ 
        if self.is_sale and self.price > 0 and self.sale_price > 0: 
            discount_amount = self.price - self.sale_price 
            discount_percent = (discount_amount / self.price) * 100 
            return round(discount_percent) 
        return 0 
    
    @property 
    def average_rating(self): 
        """ Returns the average rating for the product. """ 
        avg = ProductReview.objects.filter(product=self).aggregate(Avg('rating'))['rating__avg'] 
        return round(avg, 1) if avg else 0
    
class ProductReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Review for {self.product.name} by {self.user.username}"

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='product', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    