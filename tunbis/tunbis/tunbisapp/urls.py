from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name="index"),
    path('dogumgunu',views.birthday,name="birthday"),
    path('atama-istihdam/', views.personnel_assignment, name='personnel_assignment'),
    path('tebs/<slug:slug>',views.details,name='card_details'),

]

 