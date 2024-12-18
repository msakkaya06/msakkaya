from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name="personel_index"),
    path('atama',views.assignment,name="personel_atama"),
    path('personel-islemleri',views.personnel_operations,name="personnel_operations"),
    path('personel-islemleri/sicil_ara/', views.search_registration_number, name="search_registration_number"),
    path('personel-islemleri/ad_soyad_ara/', views.search_name, name="search_name"),
    path('personel-islemleri/tumu/', views.search_all, name="search_all"),




]

 