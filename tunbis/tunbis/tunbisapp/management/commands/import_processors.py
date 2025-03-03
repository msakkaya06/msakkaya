from django.core.management.base import BaseCommand
import pandas as pd
from django.utils import timezone
from tunbisapp.models import Computer_Informations  # Modelinizi doğru şekilde import edin

class Command(BaseCommand):
    help = 'Imports processor data from an Excel file and updates Computer_Informations model'

    def handle(self, *args, **kwargs):
        # Excel dosyasını oku
        df = pd.read_excel('processors.xlsx')  # Excel dosya yolunu belirtin

        # Her bir satırı işle
        for index, row in df.iterrows():
            # İşlemci adını al ve temizle (trim + küçük harfe çevir)
            processor_name = str(row["Name"]).strip().lower()

            # İlgili bilgisayar kayıtlarını bul (tüm eşleşen kayıtlar)
            computers = Computer_Informations.objects.filter(
                processor_name__icontains=processor_name
            )

         
            if computers.exists():
                # Eğer kayıtlar bulunursa, tümünü güncelle
                for computer in computers:
                    computer.number_of_cores = row["Core"]
                    computer.max_clock_speed_ghz = row["GHz"]
                    computer.updated_date = timezone.now()
                    computer.save()
                    self.stdout.write(self.style.SUCCESS(f'Updated existing record: {computer.processor_name}'))