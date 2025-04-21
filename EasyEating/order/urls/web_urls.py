
from django.urls import path
from .. import views


urlpatterns = [
    path('',views.web_views.index,name='order_index'),
    path('add_to_cart',views.web_views.add_to_cart,name='add_to_cart'),
    path('cart',views.web_views.cart,name='cart'),
    path('cart_to_order/<int:cart_id>',views.web_views.cart_to_order, name='cart_to_order'),
    

    
]