from django.core.management.base import BaseCommand
import pandas as pd
from tunbisapp.models import PrinterScannerInformation, Unit  # Modellerinizi doğru uygulama adıyla içe aktarın

class Command(BaseCommand):
    help = 'Imports data from printer_scanner.xlsx into the PrinterScannerInformation model'

    def handle(self, *args, **kwargs):
        try:
            # Excel dosyasını oku
            file_path = 'printer_scanner.xlsx'  # Dosya adını uygun şekilde güncelleyin
            df = pd.read_excel(file_path)

            # Her bir satırı işle
            for index, row in df.iterrows():
                try:
                    # Unit ilişkisini kontrol et ve al
                    unit = Unit.objects.get(id=row['unit'])

                    # PrinterScannerInformation modeli için bir nesne oluştur veya güncelle
                    obj, created = PrinterScannerInformation.objects.update_or_create(
                        device_name=row['device_name'],  # Benzersiz alan olarak "device_name" kullanıyoruz
                        defaults={
                            'device_type': row['device_type'],
                            'manufacturer': row['manufacturer'],
                            'model': row['model'],
                            'serial_number': row['serial_number'],
                            'unit': unit,
                            'ip_address': row['ip_address'],
                            'mac_address': row['mac_adress'],
                            'network_used': row['network_used'],
                            'connection_interface': row['connection_interface'],
                            'image': row['image'],
                        }
                    )

                    # Başarı durumunu yazdır
                    if created:
                        self.stdout.write(self.style.SUCCESS(f"'{obj.device_name}' başarıyla eklendi."))
                    else:
                        self.stdout.write(self.style.SUCCESS(f"'{obj.device_name}' başarıyla güncellendi."))

                except Unit.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f"Unit ID {row['unit']} bulunamadı. Bu satır atlandı."))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Bir hata oluştu: {str(e)}"))
