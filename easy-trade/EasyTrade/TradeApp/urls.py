# myapp/urls.py
from django.urls import path
from .views import fetch_binance_data

urlpatterns = [
    path('fetch-binance-data/', fetch_binance_data, name='fetch_binance_data'),
]
