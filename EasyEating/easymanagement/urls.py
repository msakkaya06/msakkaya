
from django.urls import path
from . import views

from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('',views.index,name='management_index'),
    path('dashboard',views.management, name='dashboard'),
    path('desk',views.desk, name='management_desk'),
    path('create_desk',views.create_desk, name='create_desk'),
    path('desk_details',views.desk_details, name='desk_details'),
    path('produce',views.produce, name='management_produce'),
    path('produce_update/<int:id>',views.produce_update, name='produce_update'),
    path('create_produce/<int:produce_type>',views.create_produce, name='create_produce'),
    path('order_details/<int:desk_id>',views.order_details, name='order_details'),
    path('mark_item_as_served/<int:order_item_id>/', views.mark_item_as_served, name='mark_item_as_served'),
    path('mark_all_items_as_served/<int:order_id>/', views.mark_all_items_as_served, name='mark_all_items_as_served'),
    path('checkout/<int:order_id>/', views.checkout, name='checkout'),
    path('sales-management/', views.sales_management, name='sales_management'),
    path('sales/', views.sales_view, name='sales_view'),
    path('finance/', views.finance_dashboard, name='finance_dashboard'),
    path('payment-screen/', views.payment_screen, name='payment_screen'),
    path('payment/<int:order_id>/', views.payment_view, name='payment_view'),
    path('process_payment/<int:order_id>/', views.process_payment, name='process_payment'),


   

] + static (settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)