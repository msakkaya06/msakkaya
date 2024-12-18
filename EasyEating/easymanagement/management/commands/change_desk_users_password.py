from django.core.management.base import BaseCommand
from easymanagement.models import EEUser
from django.contrib.auth.hashers import make_password

class Command(BaseCommand):
    help = 'is_desk True olan tüm kullanıcıların şifresini toplu olarak değiştirir'

    def handle(self, *args, **kwargs):
        new_password = "kolaymasa"
        desk_users = EEUser.objects.filter(is_desk=True)
        for user in desk_users:
            user.password=make_password(new_password)
            self.stdout.write(self.style.SUCCESS(f"kullanıcının şifresi.{user.password} "))
            user.save()
        self.stdout.write(self.style.SUCCESS(f"{desk_users.count()} kullanıcının şifresi başarıyla güncellendi."))
