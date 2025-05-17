from rest_framework import serializers
from cloud.models import Folder

class FolderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = ["id", "name", "parent", "created_at"]
