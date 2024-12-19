from django.core.management.base import BaseCommand
import pandas as pd
from django.utils.dateparse import parse_date
from tunbisapp.models import TebsUser, Unit  # Unit modelini de dahil ettik

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
            is_passive = is_passive_str == 'evet'

            # Unit ismini bul veya oluştur
            unit_name = row['unit']
            unit = None
            if pd.notna(unit_name):  # Eğer unit alanı boş değilse
                unit, created = Unit.objects.get_or_create(name=unit_name)

            # TebsUser modelinde kullanıcıyı oluştur veya güncelle
            tebs_user, created = TebsUser.objects.update_or_create(
                registration_number=row['registration_number'],
                defaults={
                    'first_name': row['first_name'],
                    'last_name': row['last_name'],
                    'rank': row['rank'],
                    'birthday': parse_date(str(row['birthday'])),
                    'telephone_number': row['telephone_number'],
                    'is_passive': is_passive,
                    'passive_description': row['passive_description'],
                    'temp_duty_station': row['temp_duty_station'],
                    'unit': unit,  # ForeignKey olarak unit bilgisi atanıyor
                }
            )

            # Yeni oluşturulan kullanıcı için şifre ayarla
            if created:
                tebs_user.set_password('Pp123456')
                tebs_user.save()

        self.stdout.write(self.style.SUCCESS('Data import completed successfully.'))
