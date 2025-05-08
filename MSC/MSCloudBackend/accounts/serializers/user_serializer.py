from rest_framework import serializers
from accounts.models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(read_only=True)
    groups = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = [
            'id', 'username', 'email',
            'first_name', 'last_name', 'full_name',
            'groups', 'created_at'
        ]

    def get_groups(self, obj):
        return [group.name for group in obj.groups.all()]
