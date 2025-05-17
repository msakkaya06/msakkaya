from rest_framework import serializers
from cloud.models import File

class FileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ["id", "name", "file", "folder", "uploaded_at"]
