import os
import qrcode
import base64
from django.core.management.base import BaseCommand
from django.conf import settings
from easymanagement.models import EEUser
from rest_framework.authtoken.models import Token
from io import BytesIO
from pyzbar.pyzbar import decode
from PIL import Image

class Command(BaseCommand):
    help = "QR Kod okuyup kosnola yazdırır"

    def handle(self, *args, **kwargs):

       img = Image.open('img\qr_codes\ekin-kebap-masa-1_qr.png')
       result = decode(img)
       for qr in result:
            print(qr.data.decode())
