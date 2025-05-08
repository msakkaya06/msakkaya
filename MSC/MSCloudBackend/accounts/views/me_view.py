from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from accounts.serializers.user_serializer import UserSerializer
from accounts.serializers.profile_serializers import UpdateProfileSerializer

class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = UpdateProfileSerializer(request.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Profil başarıyla güncellendi"}, status=status.HTTP_200_OK)

    def patch(self, request):
        serializer = UpdateProfileSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Profil başarıyla güncellendi"}, status=status.HTTP_200_OK)
