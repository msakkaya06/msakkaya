from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from cloud.serializers.folder_list import FolderListSerializer
from cloud.services.folder_list_service import FolderListService

class FolderListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        parent_id = request.query_params.get("parent_id")

        if parent_id == "null":
            parent = None
        elif parent_id is not None:
            try:
                parent = request.user.folders.get(id=parent_id)
            except:
                return Response({"error": "Klasör bulunamadı."}, status=status.HTTP_404_NOT_FOUND)
        else:
            parent = None

        folders = FolderListService.get_user_folders(request.user, parent)
        serializer = FolderListSerializer(folders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
