from django import template
from tunbisapp.models import Reservation
from django.db.models import Sum


register = template.Library()

@register.filter
def get_device_type_current_stock(device_type):
    # Bu, cihaz tipine göre depodaki mevcut cihaz sayısını döndürecektir.
    # Örnek olarak sadece is_allocated=False olan rezervasyonları sayıyoruz
    available_stock = Reservation.objects.filter(device_type=device_type, is_allocated=False).aggregate(Sum('quantity'))
    return available_stock.get('quantity__sum', 0)  # Eğer null ise 0 döner
