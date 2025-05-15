from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings

class Folder(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE, related_name="subfolders")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="folders")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("parent", "name", "owner")
        ordering = ["-created_at"]

class File(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to="uploads/")  # sonra dinamik yapacağız
    folder = models.ForeignKey(Folder, null=True, blank=True, on_delete=models.CASCADE, related_name="files")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="files")
    is_shared = models.BooleanField(default=False)
    shared_with = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="shared_files")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-uploaded_at"]

    def get_extension(self):
        return self.name.split(".")[-1].lower()
