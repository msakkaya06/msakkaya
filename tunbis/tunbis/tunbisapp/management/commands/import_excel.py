from django.core.management.base import BaseCommand
import pandas as pd
from django.utils.dateparse import parse_date
from tunbisapp.models import TebsUser 

class Command(BaseCommand):
    help = 'Imports data from an Excel file'

    def handle(self, *args, **kwargs):
        # Excel dosyasını oku
        df = pd.read_excel('user.xlsx')  # Excel dosya yolunu belirtin

        # Her bir satırı işle
        for index, row in df.iterrows():
            # is_passive alanını string olarak al ve küçük harfe dönüştür
            is_passive_str = str(row['is_passive']).lower().strip()
            
            # String değeri boolean değere dönüştür
            if is_passive_str == 'evet':
                is_passive = True
            else:
                is_passive = False

            # TebsUser modeli için bir nesne oluştur
            tebs_user = TebsUser(
                registration_number=row['registration_number'],
                first_name=row['first_name'],
                last_name=row['last_name'],
                rank=row['rank'],
                birthday=row['birthday'],
                telephone_number=row['telephone_number'],
                is_passive=is_passive,
                passive_description=row['passive_description'],
                temp_duty_station=row['temp_duty_station'],
                
            )
            
            # Password'u ayarla
            tebs_user.set_password('Pp123456')
            
            # Nesneyi veritabanına kaydet
            tebs_user.save()
