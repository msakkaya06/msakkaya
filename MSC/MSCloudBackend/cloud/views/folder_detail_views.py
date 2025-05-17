from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from cloud.models import Folder
from cloud.serializers.folder_detail_serializers import FolderDetailSerializer


class FolderDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        try:
            folder = Folder.objects.get(id=pk, owner=request.user)
        except Folder.DoesNotExist:
            return Response({"error": "Klasör bulunamadı."}, status=status.HTTP_404_NOT_FOUND)

        serializer = FolderDetailSerializer(folder)
        return Response(serializer.data, status=status.HTTP_200_OK)
