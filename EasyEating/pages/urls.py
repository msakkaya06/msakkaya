from django.urls import path
from . import views




urlpatterns = [
    path('',views.index,name="index"),
    path('index',views.index),
    path('contact',views.contact),
    path('about',views.about),
]