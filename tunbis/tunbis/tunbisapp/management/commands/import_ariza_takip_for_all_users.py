# myapp/management/commands/assign_group_to_users.py

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from tunbisapp.models import TebsUser

class Command(BaseCommand):
    help = 'Assign users with IDs between 1 and 1609 to group 4'

    def handle(self, *args, **kwargs):
        # Grubu al
        try:
            group = Group.objects.get(id=4)
        except Group.DoesNotExist:
            self.stdout.write(self.style.ERROR('Group with ID 4 does not exist'))
            return

        # Kullanıcıları al (ID 1 ile 1609 arasındaki)
        users = TebsUser.objects.filter(id__gte=1, id__lte=1609)

        # Kullanıcıları gruba ekle
        users_added = 0
        for user in users:
            user.groups.add(group)
            users_added += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully added {users_added} users to group ID 4'))

