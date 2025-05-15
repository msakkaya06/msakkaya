from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from cloud.serializers.folder_create_serializers import FolderCreateSerializer



class CreateFolderAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = FolderCreateSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            folder = serializer.save()
            return Response({"message": "Klasör oluşturuldu.", "id": folder.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
