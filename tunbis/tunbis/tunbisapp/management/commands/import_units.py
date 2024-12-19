from django.core.management.base import BaseCommand
import pandas as pd
from tunbisapp.models import Unit  # Unit modelinizi doğru uygulama adıyla içe aktarın

class Command(BaseCommand):
    help = 'Imports data from unit.xlsx into the Unit model'

    def handle(self, *args, **kwargs):
        try:
            # Excel dosyasını oku
            df = pd.read_excel('unit.xlsx')  # Dosya adını uygun şekilde güncelleyin

            # Her bir satırı işle
            for index, row in df.iterrows():
                # Unit modeli için bir nesne oluştur veya güncelle
                unit, created = Unit.objects.update_or_create(
                    id=row['Id'],  # Benzersiz `id` ile eşleşen kayıt arar
                    defaults={
                        'name': row['name'],
                        'parent_unit': row['parent_unit'] if not pd.isna(row['parent_unit']) else None,
                        'super_unit': bool(row['super_unit']),
                        'is_active': bool(row['is_active']),
                    }
                )

                # Başarı durumunu yazdır
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Unit '{unit.name}' başarıyla eklendi."))
                else:
                    self.stdout.write(self.style.SUCCESS(f"Unit '{unit.name}' başarıyla güncellendi."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Bir hata oluştu: {str(e)}"))
