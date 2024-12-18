from django.core.management.base import BaseCommand
import pandas as pd
from django.utils.dateparse import parse_date
from tunbisapp.models import Personnel_Assignment

class Command(BaseCommand):
    help = 'Imports data from an Excel file'

    def handle(self, *args, **kwargs):
        # Excel dosyasını oku
        df = pd.read_excel('atama.xlsx')  # Excel dosya yolunu belirtin

        # Her bir satırı işle
        for index, row in df.iterrows():
            # Peronel Atama modeli için bir nesne oluştur
            data = Personnel_Assignment(
                national_identity_number=row["T.C. No"],
                registration_number=row['SİCİL'],
                rank=row['RÜTBE'],
                first_last_name=row["ADI SOYADI"],
                assigned_unit=row["ATANDIĞI BİRİM"]
            )   
            # Nesneyi veritabanına kaydet
            data.save()
