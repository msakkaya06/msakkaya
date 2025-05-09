from rest_framework import serializers

class MakeAdminSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
