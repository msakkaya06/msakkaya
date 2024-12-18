from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name="idari_buro_index"),
    path('buro-atama',views.unit_assignment,name="idariburo_unit_assignment"),




]

 