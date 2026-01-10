from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='staff.users'),
    path('add/', views.add, name='staff.add'),
    path('edit/<int:id>/', views.edit, name='staff.edit'),
    path('view/<int:id>/', views.view, name='staff.view'),
    path('delete/<int:id>/', views.delete, name='staff.delete'),

]
