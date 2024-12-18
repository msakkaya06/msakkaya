import os
import qrcode
import uuid
import base64
from django.core.management.base import BaseCommand
from django.conf import settings
from easymanagement.models import EEUser  # EEUser modelini import edin
from io import BytesIO
from django.core.files.base import ContentFile

class Command(BaseCommand):
    help = "EEUser verilerini tarayarak sadece token'ı kaydeder ve QR kodunu dizine kaydeder."

    def handle(self, *args, **kwargs):
        users = EEUser.objects.filter(is_desk=True)  # Sadece masa kullanıcılarını seçiyoruz
        if not users.exists():
            self.stdout.write(self.style.WARNING("Masa kullanıcısı bulunamadı."))
            return

        for user in users:
            # Benzersiz bir token oluştur
            while True:
                raw_token = f"{user.username}:{uuid.uuid4()}"
                encoded_token = base64.urlsafe_b64encode(raw_token.encode()).decode()
                if not EEUser.objects.filter(token=encoded_token).exists():
                    break  # Benzersiz bir token bulunduysa döngüyü sonlandır

            user.token = encoded_token  # Token'i kullanıcıya atıyoruz

            # QR kod URL'sini oluştur
            login_url = f"http://192.168.137.1:8080/account/desk-login?username={user.username}&token={user.token}"

            # QR kodu oluştur
            qr_image = qrcode.make(login_url)
            buffer = BytesIO()
            qr_image.save(buffer, format="PNG")  # QR kodu buffer'a PNG formatında kaydediyoruz

            # Dosya adı
            file_name = f"{user.username}_qr.png"
            
            # Dosyanın kaydedileceği yolu belirleyelim
            qr_code_directory = os.path.join(settings.MEDIA_ROOT, 'qr_codes')  # QR kodlar için dizin
            if not os.path.exists(qr_code_directory):
                os.makedirs(qr_code_directory)  # Dizin yoksa oluştur

            image_path = os.path.join(qr_code_directory, file_name)

            # QR kodunu dosyaya kaydet
            with open(image_path, 'wb') as f:
                f.write(buffer.getvalue())

      
            user.save()  # Kullanıcıyı kaydediyoruz

            self.stdout.write(self.style.SUCCESS(f"{user.username} için benzersiz token oluşturuldu ve QR kod dosyası kaydedildi."))

        self.stdout.write(self.style.SUCCESS("Tüm kullanıcılar için benzersiz token ve QR kodlar başarıyla kaydedildi."))
