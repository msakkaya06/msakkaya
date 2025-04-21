from django.db import models
from django.core.exceptions import ValidationError
from tunbisapp.models import TebsUser
from django.contrib.auth.models import Permission

class DocumentType(models.TextChoices):
    WORD = ".docx", "Word"
    EXCEL = ".xlsx", "Excel"
    PDF = ".pdf", "Pdf"
    TEXT = ".txt", "Text"

class Folder(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(TebsUser, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name



class Document(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    content = models.TextField(null=True, blank=True)  # Online düzenlenen içerik
    file = models.FileField(upload_to='documents/%Y/%m/%d/', null=True, blank=True)  # Yüklenen dosya
    user = models.ForeignKey(TebsUser, on_delete=models.CASCADE)  # Kullanıcı bilgisi
    document_type = models.CharField(max_length=20, choices=DocumentType.choices)  # Belge türü (PDF, Word, vb.)
    folder = models.ForeignKey('Folder', null=True, blank=True, on_delete=models.SET_NULL)  # Klasör bağlantısı
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    # Metni dışa aktarmak için bir metod ekleyebiliriz
    def export_to_file(self):
        # Burada kullanıcıya dosya formatına göre dışa aktarım yapılabilir
        pass

    def clean(self):
        # Dosya uzantısını doğrulama
        file_extension = self.file.name.split('.')[-1]
        allowed_extensions = ['docx', 'xlsx', 'pdf']
        if file_extension not in allowed_extensions:
            raise ValidationError(f"Bu dosya türü izin verilen uzantılardan biri değil: {', '.join(allowed_extensions)}")

    def __str__(self):
        return self.title
    


class DocumentPermission(models.Model):
    user = models.ForeignKey(TebsUser, on_delete=models.CASCADE)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    can_edit = models.BooleanField(default=False)
    can_download = models.BooleanField(default=True)

