from django.contrib.auth.models import Group
from accounts.models import CustomUser
from accounts.constants import UserGroups

class UserService:
    @staticmethod
    def create_user(username: str, email: str, password: str, first_name: str = "", last_name: str = "") -> CustomUser:
        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        group, _ = Group.objects.get_or_create(name=UserGroups.STANDARD)
        user.groups.add(group)

        return user
