# myapp/models.py
from django.db import models
from djongo import models as djongo_models

class Symbol(models.Model):
    symbol = models.CharField(max_length=10, unique=True)
    base_asset = models.CharField(max_length=10)
    quote_asset = models.CharField(max_length=10)
    status = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.symbol


class KlineData(models.Model):
    symbol = models.ForeignKey(Symbol, on_delete=models.CASCADE)
    interval = models.CharField(max_length=5)
    open_time = models.DateTimeField()
    open_price = models.DecimalField(max_digits=20, decimal_places=8)
    high_price = models.DecimalField(max_digits=20, decimal_places=8)
    low_price = models.DecimalField(max_digits=20, decimal_places=8)
    close_price = models.DecimalField(max_digits=20, decimal_places=8)
    volume = models.DecimalField(max_digits=20, decimal_places=8)
    close_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.symbol.symbol} - {self.interval} - {self.open_time}"
    # Mum Data Bilgileri saklamak için kullanılacak


class TickerData(models.Model):
    symbol = models.ForeignKey(Symbol, on_delete=models.CASCADE)
    price_change = models.DecimalField(max_digits=20, decimal_places=8)
    price_change_percent = models.DecimalField(max_digits=5, decimal_places=2)
    weighted_avg_price = models.DecimalField(max_digits=20, decimal_places=8)
    last_price = models.DecimalField(max_digits=20, decimal_places=8)
    volume = models.DecimalField(max_digits=20, decimal_places=8)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.symbol.symbol} - {self.created_at}"
    #Bu model, son 24 saatteki fiyat değişiklikleri ile ilgili verileri saklamak için kullanılacak.

class OrderBook(djongo_models.Model):
    symbol = djongo_models.ForeignKey(Symbol, on_delete=models.CASCADE)
    last_update_id = djongo_models.BigIntegerField()
    bids = djongo_models.JSONField()  # Alım emirleri (fiyat ve miktar)
    asks = djongo_models.JSONField()  # Satım emirleri (fiyat ve miktar)
    created_at = djongo_models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.symbol.symbol} - {self.last_update_id}"
    #Bu model, belirli bir işlem çifti için güncel alım ve satım emirlerini saklar.


class RecentTrade(models.Model):
    symbol = models.ForeignKey(Symbol, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=20, decimal_places=8)
    qty = models.DecimalField(max_digits=20, decimal_places=8)
    time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.symbol.symbol} - {self.time}"
#Bu model, son yapılan işlemleri saklamak için kullanılacak.