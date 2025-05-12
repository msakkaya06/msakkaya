from django.db import models

# Accounts Models is here

from django.contrib.auth.models import AbstractUser
from django.db import models

def user_profile_upload_path(instance, filename):
    return f'profiles/user_{instance.id}/{filename}'

class CustomUser(AbstractUser):
    profile_image = models.ImageField(upload_to=user_profile_upload_path, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def __str__(self):
        return self.username

