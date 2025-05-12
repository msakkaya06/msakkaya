from rest_framework import serializers
from accounts.models import CustomUser

class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "email", "profile_image"]