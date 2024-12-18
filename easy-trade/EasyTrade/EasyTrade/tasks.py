from datetime import datetime
import requests
from celery import shared_task
from TradeApp.models import KlineData, Symbol  # Model importlarını uygun şekilde yapın

@shared_task
def fetch_kline_data(symbol_id, interval):
    try:
        # Binance API'den veri çek
        url = f'https://api.binance.com/api/v3/klines?symbol={symbol_id}&interval={interval}'
        response = requests.get(url)
        response.raise_for_status()  # HTTP hataları kontrol et
        data = response.json()

        # Verileri işleyip veritabanına kaydet
        for kline in data:
            if len(kline) >= 12:
                KlineData.objects.create(
                    symbol=Symbol.objects.get(symbol=symbol_id),
                    interval=interval,
                    open_time=datetime.fromtimestamp(kline[0] / 1000),
                    open_price=kline[1],
                    high_price=kline[2],
                    low_price=kline[3],
                    close_price=kline[4],
                    volume=kline[5],
                    close_time=datetime.fromtimestamp(kline[6] / 1000)
                )
            else:
                print(f"Skipping kline with unexpected format: {kline}")
    except Exception as e:
        # Hata mesajını logla veya yönet
        print(f"Error fetching kline data: {e}")
