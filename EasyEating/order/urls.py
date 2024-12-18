
from django.urls import path
from . import views


urlpatterns = [
    path('',views.index,name='order_index'),
    path('add_to_cart',views.add_to_cart,name='add_to_cart'),
    path('cart',views.cart,name='cart'),
    path('cart_to_order/<int:cart_id>',views.cart_to_order, name='cart_to_order'),


    
]