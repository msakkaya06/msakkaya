from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from accounts.models import CustomUser
from accounts.permissions import IsInGroup
from accounts.serializers.user_serializer import UserSerializer

class AdminUserListView(APIView):
    permission_classes = [IsInGroup("admin")]

    def get(self, request):
        users = CustomUser.objects.all().order_by("-date_joined")
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
