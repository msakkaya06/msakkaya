from cloud.models import File
from django.core.exceptions import ValidationError

class UploadFileService:
    @staticmethod
    def execute(owner, uploaded_file, folder=None):
        file_name = uploaded_file.name

        # Aynı isimde dosya var mı? (aynı klasör ve kullanıcı altında)
        exists = File.objects.filter(owner=owner, folder=folder, name=file_name).exists()
        if exists:
            raise ValidationError("Bu isimde bir dosya zaten mevcut.")

        # Oluştur
        file = File.objects.create(
            name=file_name,
            file=uploaded_file,
            folder=folder,
            owner=owner
        )
        return file
