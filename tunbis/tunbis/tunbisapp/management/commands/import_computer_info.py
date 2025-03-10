from django.core.management.base import BaseCommand
import pandas as pd
from tunbisapp.models import Computer_Informations, Unit
from django.core.files.base import ContentFile
import os

class Command(BaseCommand):
    help = 'Imports data from an Excel file for ComputerInformations model'

    def handle(self, *args, **kwargs):
        # Excel dosyasını oku
        df = pd.read_excel('computer_info.xlsx', dtype=str).fillna('')


        # Her bir satırı işle
        for index, row in df.iterrows():
            try:
                # Veriyi temizle ve hatalı değerleri düzelt
                cleaned_row = {k: (str(v).strip() if pd.notnull(v) else '') for k, v in row.items()}
        
                # Bilgisayar adıyla eşleşen bir kayıt varsa güncelle, yoksa yeni bir kayıt oluştur
                computer_info, created = Computer_Informations.objects.update_or_create(
                    computer_name=cleaned_row["Computer Name"],
                    defaults={
                        "manufacturer": cleaned_row["Manufacturer"],
                        "model": cleaned_row["Model"],
                        "number_of_processors": cleaned_row["Number of Processors"],
                        "system_type": cleaned_row["System Type"],
                        "serial_number": cleaned_row["Serial Number"],
                        "processor_name": cleaned_row["Processor Name"],
                        "number_of_cores": cleaned_row["Number of Cores"],
                        "max_clock_speed_ghz": cleaned_row["Max Clock Speed (GHz)"],
                        "graphics_card": cleaned_row["Graphics Card"],
                        "bios_version": cleaned_row["BIOS Version"],
                        "product": cleaned_row["Product"],
                        "base_board_serial_number": cleaned_row["Base Board Serial Number"],
                        "number_of_memory_slots": cleaned_row["Number of Memory Slots"],
                        "total_ram_gb": cleaned_row["Total RAM (GB)"],
                        "used_ram_slots": cleaned_row["Used RAM Slots"],
                        "ip_address": cleaned_row["IP Address"],
                        "disk_drive_model": cleaned_row["Disk Drive Model"],
                        "disk_size_gb": cleaned_row["Disk Size (GB)"],
                        "media_type": cleaned_row["Media Type"],
                        "disk_partition_name": cleaned_row["Disk Partition Name"],
                        "operating_system": cleaned_row["Operating System"],
                        "os_version": cleaned_row["OS Version"],
                        "os_build_number": cleaned_row["OS Build Number"],
                        "office_version": cleaned_row["Office Version"],
                        "office_license_status": cleaned_row["Office License Status"],
                        "disk_usage_percentage": cleaned_row["Disk Usage (%)"],
                        "ram_brands": cleaned_row["RAM Brands"],
                        "average_ram_speed": cleaned_row["Average RAM Speed"],
                        "ram_slot_types": cleaned_row["RAM Slot Types"],
                        "network_used": cleaned_row["network_used"],
                    }
                )
                # Eğer "image" adında bir sütun varsa ve değeri varsa, resmi kaydet
                if "image" in df.columns and not pd.isnull(cleaned_row["image"]):
                    image_path = cleaned_row["image"]  # Resim dosya yolu
                    # Resim dosyasını aç ve içeriğini oku
                    with open(image_path, 'rb') as f:
                        image_content = ContentFile(f.read(), os.path.basename(image_path))
                    computer_info.image.save(os.path.basename(image_path), image_content, save=True)

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error processing row {index}: {str(e)}"))

        self.stdout.write(self.style.SUCCESS("Import process completed"))
