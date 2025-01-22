# urls.py
from django.urls import path
from . import views

urlpatterns = [

    path('upload_excel/', views.upload_excel, name='upload_excel'),

]