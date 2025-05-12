from rest_framework import serializers
from accounts.models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    groups = serializers.SlugRelatedField(
        many=True,
        slug_field='name',   # 💥 ID yerine name döner
        read_only=True
    )

    class Meta:
        model = CustomUser
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'full_name',
            'groups',
            'is_superuser',
            'is_active',
            'created_at',
            'profile_image',
            'last_login',
        ]
