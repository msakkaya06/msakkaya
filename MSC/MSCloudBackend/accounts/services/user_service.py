from django.contrib.auth.models import User

class UserService:
    @staticmethod
    def create_user(username: str, email: str, password: str) -> User:
        return User.objects.create_user(username=username, email=email, password=password)
