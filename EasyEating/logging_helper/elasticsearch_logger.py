from elasticsearch import Elasticsearch
from datetime import datetime
import pytz

class ElasticsearchLogger:
    def __init__(self, host='localhost', port=9200, scheme='http', username='elastic', password='changeme'):
        # Elasticsearch bağlantısı için kimlik doğrulama bilgileri eklendi
        self.es = Elasticsearch(
            [{'host': host, 'port': port, 'scheme': scheme}],
            http_auth=(username, password) if username and password else None  # Kimlik doğrulaması
        )

    def log(self, index, data):
        """Log verisini Elasticsearch'e gönderir"""
        try:
            # Eğer timestamp UTC formatında string ise
            if isinstance(data['timestamp'], str):
                # Zaman damgasını datetime objesine çevir
                utc_time = datetime.strptime(data['timestamp'], "%b %d, %Y @ %H:%M:%S.%f")  # Örnek format: "Dec 16, 2024 @ 17:04:29.000"
                utc_time = pytz.utc.localize(utc_time)  # UTC olarak lokalize et
            elif isinstance(data['timestamp'], datetime):
                utc_time = data['timestamp'].astimezone(pytz.utc)  # Zaten datetime ise UTC'ye dönüştür

            # İstanbul zaman dilimine dönüştür
            istanbul_tz = pytz.timezone('Europe/Istanbul')  # İstanbul saati
            timestamp_istanbul = utc_time.astimezone(istanbul_tz)  # İstanbul zamanına dönüştür

            # Yeni zaman damgası
            data['timestamp'] = timestamp_istanbul.strftime("%Y-%m-%dT%H:%M:%SZ")


            # Elasticsearch'e logu gönder
            response = self.es.index(index=index, body=data)
            print(f"Log başarıyla gönderildi: {response}")
        except Exception as e:
            print(f"Log gönderme hatası: {e}")
