# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="ariza_takip_index"),
    path('ariza-kaydi-oluştur/<int:pk>', views.fault_create, name="ariza_takip_fault"),
    path('ariza-kaydi-kaydet', views.fault_create_save, name="ariza_takip_fault_save"),
    path('ariza-kaydi-takip', views.fault_tracking, name="ariza_takip_fault_tracking"),
    path('cihaz-talep', views.device_request, name="ariza_takip_device_request"),
    path('ariza-kaydi-detay/<int:pk>/', views.fault_detail, name="ariza_takip_fault_detail"),

    





    
]
