from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='home.index'),
    path('about/', views.about, name='home.about'),
    path('products-home/', views.product, name='home.products_item'),
    path('product-details/<int:id>/', views.productDetails, name='home.product_details'),
    path('shopping-cart/', views.shopCart, name='home.shopping_cart'),
    
    path('category/<str:foo>/', views.category, name='home.category'),

    path('login/', views.login_user, name='home.login_user'),
    path('register/', views.register_user, name='home.register_user'),
    path('profile/', views.profile, name='home.profile'),
    path('logout/', views.user_logout, name='home.logout_user'),

    path('review/', views.product_review, name='home.review'),

    path('cart_detail/', views.cart_detail, name='cart_detail'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update/<int:product_id>/', views.update_cart_item, name='update_cart_item'),


   path('checkout/', views.checkout, name='checkout'),
   path('order-confirm/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
]