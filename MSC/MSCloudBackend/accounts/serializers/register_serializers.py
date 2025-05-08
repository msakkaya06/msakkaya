from rest_framework import serializers
from accounts.models import CustomUser

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'first_name', 'last_name']
        extra_kwargs = {
            'password': {'write_only': True}
        }
