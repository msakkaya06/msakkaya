from cloud.models import Folder
from django.core.exceptions import ValidationError

class CreateFolderService:
    @staticmethod
    def execute(owner, name, parent=None):
        # Aynı kullanıcı ve aynı parent altında aynı isimde klasör var mı?
        exists = Folder.objects.filter(owner=owner, parent=parent, name=name).exists()
        if exists:
            raise ValidationError("Aynı klasör zaten mevcut.")

        folder = Folder.objects.create(
            name=name,
            parent=parent,
            owner=owner
        )
        return folder
