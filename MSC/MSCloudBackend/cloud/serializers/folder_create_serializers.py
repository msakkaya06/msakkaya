from rest_framework import serializers
from cloud.models import Folder
from cloud.services.folder_create_services import CreateFolderService

class FolderCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    parent_id = serializers.IntegerField(required=False, allow_null=True)

    def validate_parent_id(self, value):
        if value is not None:
            try:
                parent = Folder.objects.get(id=value, owner=self.context["request"].user)
                return parent
            except Folder.DoesNotExist:
                raise serializers.ValidationError("Üst klasör bulunamadı.")
        return None

    def create(self, validated_data):
        name = validated_data["name"]
        parent = validated_data.get("parent_id")
        user = self.context["request"].user
        return CreateFolderService.execute(owner=user, name=name, parent=parent)
