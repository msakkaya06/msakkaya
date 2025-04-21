import os
import qrcode
import base64
from django.core.management.base import BaseCommand
from django.conf import settings
from easymanagement.models import EEUser
from rest_framework.authtoken.models import Token
from io import BytesIO

class Command(BaseCommand):
    help = "Masa kullanıcıları için DRF token oluşturur ve React tabanlı login URL’lerini QR kod olarak kaydeder."

    def handle(self, *args, **kwargs):
        users = EEUser.objects.filter(is_desk=True)
        if not users.exists():
            self.stdout.write(self.style.WARNING("Masa kullanıcısı bulunamadı."))
            return

        for user in users:
            # Token oluştur veya mevcut tokenı getir
            token, created = Token.objects.get_or_create(user=user)

            # React tabanlı login redirect URL’si
            login_url = f"http://192.168.137.1:3000/login-redirect?username={user.username}&token={token.key}"

            # QR kod oluştur
            qr_image = qrcode.make(login_url)
            buffer = BytesIO()
            qr_image.save(buffer, format="PNG")

            # Dosya ismi ve yol
            file_name = f"{user.username}_qr.png"
            qr_code_directory = os.path.join(settings.MEDIA_ROOT, 'qr_codes')
            if not os.path.exists(qr_code_directory):
                os.makedirs(qr_code_directory)

            image_path = os.path.join(qr_code_directory, file_name)

            with open(image_path, 'wb') as f:
                f.write(buffer.getvalue())

            self.stdout.write(self.style.SUCCESS(
                f"{user.username} için QR kod oluşturuldu ve kaydedildi. Token: {token.key}"
            ))

        self.stdout.write(self.style.SUCCESS("Tüm masa kullanıcıları için token ve QR kodlar oluşturuldu."))
