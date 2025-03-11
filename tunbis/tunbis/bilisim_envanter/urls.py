# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="envanter_index"),
    path('dashboard', views.index, name="envanter_index"),
    path('bilgisayar-istatistik', views.computer_statistics, name="computer_statistics"),

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
    path('birim-bilgisayar-liste/<int:pk>/', views.computer_detail_for_unit, name='computer_detail_for_unit'),
    path('import-computer-info/', views.import_computer_info, name='import_computer_info'),
    path('yazici-tarayici-ekle/', views.add_printer_scanner, name='add_printer_scanner'),
    path('talepler/', views.all_device_requests, name="all_device_requests"),
    path('talep-ekle/', views.device_request, name="device_request_create"),
    path('talep-istatistik/', views.device_request_summary, name="device_request_summary"),
    path('talep-istatistik/pdf/', views.device_request_pdf, name="device_request_pdf"),
    path('rezerv-ekle/', views.add_reservation, name='add_reservation'),
    path('rezerv-düzenle/<int:pk>/', views.edit_reservation, name='edit_inventory'),
    path('rezerv-sil/<int:pk>/', views.delete_reservation, name='delete_inventory'),
    path('depo/', views.warehouse_inventory, name='warehouse_inventory'),
    path('planlama/', views.planning_list, name='planning_list'),
    path('planlama/teslim/<int:plan_id>/', views.delivered, name='delivered'),
    path('planlama/tahsis/', views.allocation_screen, name='allocation'),
    path('get_unit_data/<int:unit_id>/', views.get_unit_data, name='get_unit_data'),
    path('planlama/tahsis/duzenle/<int:plan_id>/', views.edit_plan, name='edit_plan'),
    path('planlama/tahsis/iptal/<int:plan_id>/', views.cancel_plan, name='cancel_plan'),
    path('bilisim-envanter/planlama/pdf/', views.planning_pdf, name='planning_pdf'),
    path("update_device_request/", views.update_device_request, name="update_device_request"),





    
]
