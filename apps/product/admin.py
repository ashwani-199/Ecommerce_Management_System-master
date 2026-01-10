from django.contrib import admin
from apps.product.models import Product, ProductCategory, ProductImage, ProductReview


class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'image', 'created_at', 'updated_at']

    


class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'brand_name', 'price' ,'stock', 'user' ,'categories']

admin.site.register(Product,ProductAdmin)
admin.site.register(ProductCategory)
admin.site.register(ProductImage,ProductImageAdmin)
admin.site.register(ProductReview)