from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from cloud.serializers.file_upload_serializers import FileUploadSerializer




class FileUploadAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = FileUploadSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            file = serializer.save()
            return Response({"message": "Dosya yüklendi.", "id": file.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
