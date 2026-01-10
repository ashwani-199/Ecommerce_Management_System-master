from .models import Product, ProductCategory, ProductImage, ProductReview
from rest_framework import serializers


class ProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'brand_name', 'price','stock','image','user','categories']


# from apps.users.models import User
# from apps.users.serializers import UserSerializer

# class ProductCategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ProductCategory
#         fields = ['id', 'name', 'created_at', 'updated_at']

# class ProductSerializer(serializers.ModelSerializer):
#     vendor = VendorProfileSerializer()
#     categories = ProductCategorySerializer()

#     class Meta:
#         model = Product
#         fields = ['id','vendor', 'categories', 'name', 'description', 'price', 'quantity', 'created_at', 'updated_at']

#     def create(self, validated_data):
#         vendor_data = validated_data.pop('vendor')
#         categories_data = validated_data.pop('categories')
#         vendor_instance, _ = VendorProfile.objects.get_or_create(**vendor_data)
#         categories_instances = [ProductCategory.objects.get_or_create(**category_data)[0] for category_data in categories_data]
#         product = Product.objects.create(vendor=vendor_instance, **validated_data)
#         product.categories.set(categories_instances)
#         return product
    
#     def update(self, instance, validated_data):
#         vendor_data = validated_data.pop('vendor')
#         categories_data = validated_data.pop('categories')
#         vendor_instance, _ = VendorProfile.objects.get_or_create(**vendor_data)
#         categories_instances = [ProductCategory.objects.get_or_create(**category_data)[0] for category_data in categories_data]
#         instance.vendor = vendor_instance
#         instance.categories.set(categories_instances)
#         instance.name = validated_data.get('name', instance.name)
#         instance.description = validated_data.get('description', instance.description)
#         instance.price = validated_data.get('price', instance.price)
#         instance.quantity = validated_data.get('quantity', instance.quantity)
#         instance.save()
#         return instance
        
# class ProductReviewSerializer(serializers.ModelSerializer):
#     product = ProductCategorySerializer()
#     user = UserSerializer()
#     class Meta:
#         model = ProductReview
#         fields = ['id','product', 'user', 'rating', 'comment', 'created_at', 'updated_at']

#     def create(self, validated_data):
#         product_data = validated_data.pop('product')
#         user_data = validated_data.pop('user')
#         product_instance, _ = Product.objects.get_or_create(**product_data)
#         user_instance, _ = User.objects.get_or_create(**user_data)
#         review = ProductReview.objects.create(product=product_instance, user=user_instance, **validated_data)
#         return review
    
#     def update(self, instance, validated_data):
#         product_data = validated_data.pop('product')
#         user_data = validated_data.pop('user')
#         product_instance, _ = Product.objects.get_or_create(**product_data)
#         user_instance, _ = User.objects.get_or_create(**user_data)
#         instance.product = product_instance
#         instance.user = user_instance
#         instance.rating = validated_data.get('rating', instance.rating)
#         instance.comment = validated_data.get('comment', instance.comment)
#         instance.save()
#         return instance()
     

    
# class ProductVariantSerializer(serializers.ModelSerializer):
#     product = ProductSerializer()
#     class Meta:
#         model = ProductVariant
#         fields = ['id', 'product', 'name', 'price', 'quantity', 'created_at', 'updated_at']

#     def create(self, validated_data):
#         product_data = validated_data.pop('product')
#         products, _ = Product.objects.get_or_create(**product_data)
#         product_varient = ProductVariant.objects.create(product = products, **validated_data)
#         return product_varient
    
#     def update(self, instance, validated_data):
#         product_data = validated_data.pop('product')
#         product_instance, _ = Product.objects.get_or_create(**product_data)
#         instance.product = product_instance
#         instance.name = validated_data.get('name', instance.name)
#         instance.price = validated_data.get('price', instance.price)
#         instance.quantity = validated_data.get('quantity', instance.quantity)
#         instance.save()
#         return instance


# class ProductImageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ProductImage
#         fields = ['id', 'product', 'image', 'created_at', 'updated_at']

#     def create(self, validated_data):
#         return ProductImage.objects.create(**validated_data)

#     def update(self, instance, validated_data):
#         instance.product = validated_data.get('product', instance.product)
#         instance.image = validated_data.get('image', instance.image)
#         instance.save()
#         return instance