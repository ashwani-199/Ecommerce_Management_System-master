# from rest_framework import serializers
# from .models import  Order, OrderHistory, OrderItem, OrderStatus
# from clients.serializers import ClientProfileSerializer
# from clients.models import ClientProfile
# from product.models import Product
# from product.serializers import ProductSerializer


# class OrderSerializer(serializers.ModelSerializer):
#     client = ClientProfileSerializer()
#     class Meta:
#         model = Order
#         fields = ['id', 'client', 'total_amount', 'status', 'created_at', 'updated_at']

#     def create(self, validated_data):
#         client_data = validated_data.pop('client')
#         client_profile =ClientProfile.objects.create(**client_data)
#         order_data = Order.objects.create(client = client_profile, **validated_data)
#         return order_data
    
#     def update(self, instance, validated_data):
#         client_data = validated_data.pop('client')
#         client_serializer = ClientProfileSerializer(instance.client, data=client_data, partial=True)
#         if client_serializer.is_valid():
#             client_serializer.save()
        
#         instance.total_amount = validated_data.get('total_amount', instance.total_amount)
#         instance.status = validated_data.get('status', instance.status)
#         instance.save()
#         return instance
    

# class OrderHistorySerializer(serializers.ModelSerializer):
#     order = OrderSerializer()
#     class Meta:
#         model = OrderHistory
#         fields = ['id', 'order', 'status', 'created_at']

#     def create(self, validated_data):
#         order_data = validated_data.pop('order')
#         orders = Order.objects.create(**order_data)
#         order_history = OrderHistory.objects.create(order = orders, **validated_data) 
#         return order_history
    
#     def update(self, instance, validated_data):
#         order_data = validated_data.pop('order')
#         order_serializer = OrderHistorySerializer(instance.client, data=order_data, partial = True)
#         if order_serializer.is_valid():
#             order_serializer.save()
#         instance.status = validated_data.get('status', instance.status)
#         instance.save()
#         return instance
    


# class OrderItemSerializer(serializers.ModelSerializer):
#     order = OrderSerializer()
#     product = ProductSerializer()
#     class Meta:
#         model = OrderItem
#         fields = ['id', 'order', 'product', 'quantity', 'price', 'total_price']

#     def create(self, validated_data):
#         order_data = validated_data.pop('order')
#         product_data = validated_data.pop('product')
#         orders = Order.objects.create(**order_data)
#         products = Product.objects.create(**product_data)
#         order_item = OrderItem.objects.create(order=orders, product = products, **validated_data)

#         return order_item
    
#     def update(self, instance, validated_data):
#         order_data = validated_data.pop('order')
#         product_data = validated_data.pop('product')
#         order_instance, _ = Order.objects.get_or_create(**order_data)
#         product_instance, _ = Product.objects.get_or_create(**product_data)
#         instance.order = order_instance
#         instance.product = product_instance
#         instance.quantity = validated_data.get('quantity', instance.quantity)
#         instance.price = validated_data.get('price', instance.price)
#         instance.total_price = validated_data.get('total_price', instance.total_price)
#         instance.save()
#         return instance
    
# class OrderStatusSerialize(serializers.ModelSerializer):
#     order = OrderSerializer()
#     class Meta:
#         model = OrderStatus
#         fields = ['id', 'order', 'status', 'timestamp']

#     def create(self, validated_data):
#         order_data = validated_data.pop('order')
#         orders = Order.objects.create(**order_data)
#         order_status = OrderStatus.objects.create(order = orders, **validated_data)
#         return order_status
    
#     def update(self, instance, validated_data):
#         order_data = validated_data.pop('order')
#         instance.order = order_data
#         instance.status = validated_data.get('status', instance.status)
#         instance.timestamp = validated_data.get('timestamp', instance.timestamp)
#         instance.save()
#         return instance