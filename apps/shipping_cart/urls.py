from django.urls import path
from . import views


urlpatterns = [
   path('', views.cart_index, name='shipping.index'),
   path('add-cart/', views.cart_add, name='shipping.add'),
   path('edit-cart/', views.update_cart, name='shipping.edit'),
   path('delete-cart/', views.delete_cart, name='shipping.delete'),
   
]