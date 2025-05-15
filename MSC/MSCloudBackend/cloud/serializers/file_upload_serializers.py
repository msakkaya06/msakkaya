from rest_framework import serializers
from cloud.models import File, Folder
from cloud.services.file_services import UploadFileService

class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()
    folder_id = serializers.IntegerField(required=False, allow_null=True)

    def validate_folder_id(self, value):
        if value is not None:
            try:
                return Folder.objects.get(id=value, owner=self.context["request"].user)
            except Folder.DoesNotExist:
                raise serializers.ValidationError("Klasör bulunamadı.")
        return None

    def create(self, validated_data):
        folder = validated_data.get("folder_id")
        user = self.context["request"].user
        uploaded_file = validated_data["file"]
        return UploadFileService.execute(owner=user, uploaded_file=uploaded_file, folder=folder)
