from django.urls import path
from . import views


urlpatterns = [
   path('', views.index, name='orders.index'),
   path('edit/<int:id>/', views.edit, name='orders.edit'),
   path('view/<int:id>/', views.view, name='orders.view'),
   path('delete/<int:id>/', views.delete, name='orders.delete'),
   path('order-item/', views.order_item_index, name='order_item.index'),
   
]