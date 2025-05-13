from django.core.management.base import BaseCommand
from accounts.models import CustomUser
from faker import Faker
import random

class Command(BaseCommand):
    help = "Fake kullanıcı üretir (varsayılan: 100 adet)"

    def add_arguments(self, parser):
        parser.add_argument('--count', type=int, default=100, help='Kaç adet kullanıcı oluşturulacak')

    def handle(self, *args, **options):
        count = options['count']
        fake = Faker("tr_TR")

        created = 0
        for _ in range(count):
            username = fake.unique.user_name()
            email = fake.unique.email()
            first_name = fake.first_name()
            last_name = fake.last_name()

            if not CustomUser.objects.filter(username=username).exists():
                CustomUser.objects.create_user(
                    username=username,
                    email=email,
                    password="12345678",  # default şifre
                    first_name=first_name,
                    last_name=last_name
                )
                created += 1

        self.stdout.write(self.style.SUCCESS(f"✅ {created} fake kullanıcı oluşturuldu."))
