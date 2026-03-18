from django.urls import path
from . import views

app_name = "shop"

urlpatterns = [
    path('', views.shop_home, name='shop_home'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart'),
path('product/<slug:slug>/', views.product_detail, name='product_detail'),
path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
]