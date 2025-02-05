# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="envanter_index"),
    path('istatistik', views.index, name="envanter_index"),
    path('ariza-takip/', views.fault_tracking, name="fault_tracking"),
    path('ariza-takip/icmal', views.fault_summary, name="fault_summary"),
    path('ariza-takip/<int:pk>/', views.fault_tracking_detail, name="fault_tracking_detail"),
    path('bilgisayar/', views.computer, name="envanter_computer"),
    path('bilgisayar/<int:pk>/', views.computer_detail, name="envanter_computer_detail"),
    path('search-name/', views.search_name, name='search_name'),
    path('search-computer/', views.search_computer, name='search_computer'),
    path('search-serial/', views.search_serial, name='search_serial'),
    path('search-unit/', views.search_unit, name='search_unit'),
    path('search-device/', views.search_device, name='search_device'),
    path('save_device_action/', views.save_device_action, name='save_computer_action'),
    path('search-user/', views.search_user, name='search_user'),
    path('fault-record-create/', views.fault_record_create, name='fault_record_create'),
    path('search-name-fault/', views.search_name_fault, name='search_name_fault'),
     path('finalize_fault_action/', views.finalize_fault_action, name='finalize_fault_action'),
    path('yazici_tarayici/', views.printer_scanner_list, name="printer_scanner_list"),
    path('yazici_tarayici/<int:pk>/', views.printer_scanner_detail, name="printer_scanner_detail"),
    path('search-printer-name/', views.search_printer_name, name='search_printer_name'),
    path('search-printer-serial/', views.search_printer_serial, name='search_printer_serial'),
    path('search-printer-unit/', views.search_printer_unit, name='search_printer_unit'),
    path('computer-detail-for-unit/<int:pk>/', views.computer_detail_for_unit, name='computer_detail_for_unit'),
    path('import-computer-info/', views.import_computer_info, name='import_computer_info'),
    path('yazici-tarayici-ekle/', views.add_printer_scanner, name='add_printer_scanner'),
    
]
