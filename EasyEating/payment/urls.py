
from django.urls import path
from . import views


urlpatterns = [
    path('',views.index,name='payment_index'),
    path('checkout/<int:order_id>/', views.checkout, name='checkout'),
    path('<int:order_id>/', views.payment, name='payment'),

   

]