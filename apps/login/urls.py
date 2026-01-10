from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('myaccount/', views.profile, name='myaccount'),
    path('forgot-password/', views.forgotPassword, name='forgot_password'),
    path('reset-password/<token>/', views.passwordReset, name='reset_password'),


]
