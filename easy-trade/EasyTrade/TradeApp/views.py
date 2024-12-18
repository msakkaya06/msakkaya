from django.shortcuts import render
from pymongo import MongoClient

# myapp/views.py
from django.http import JsonResponse
import requests

def fetch_binance_data(request):
    url = "https://api.binance.com/api/v3/klines"
    params = {
        "symbol": "BTCUSDT",
        "interval": "1h",
        "limit": 50  # Test için 5 veri çekelim
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    # İsteği başarıyla aldıysan, dönen veriyi JSON olarak döndürelim
    return JsonResponse(data, safe=False)


