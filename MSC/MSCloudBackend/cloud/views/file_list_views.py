from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from cloud.serializers.file_list import FileListSerializer
from cloud.models import Folder
from cloud.services.file_list_service import FileListService

class FileListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        folder_id = request.query_params.get("folder_id")

        if folder_id == "null":
            folder = None
        elif folder_id is not None:
            try:
                folder = request.user.folders.get(id=folder_id)
            except Folder.DoesNotExist:
                return Response({"error": "Klasör bulunamadı."}, status=status.HTTP_404_NOT_FOUND)
        else:
            folder = None

        files = FileListService.get_user_files(request.user, folder)
        serializer = FileListSerializer(files, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
