from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='customer.index'),
    path('edit/<int:id>/', views.edit, name='customer.edit'),
    path('view/<int:id>/', views.view, name='customer.view'),
    path('delete/<int:id>/', views.delete, name='customer.delete'),

]
