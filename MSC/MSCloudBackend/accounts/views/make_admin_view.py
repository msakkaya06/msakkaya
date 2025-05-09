from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import Group
from accounts.serializers.admin_assigned_serializers import MakeAdminSerializer
from accounts.models import CustomUser
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsInGroup


class MakeAdminView(APIView):
    permission_classes = [IsAuthenticated, IsInGroup("admin")]

    def post(self, request):
        serializer = MakeAdminSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_id = serializer.validated_data["user_id"]
        try:
            target_user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response({"error": "Kullanıcı bulunamadı"}, status=status.HTTP_404_NOT_FOUND)

        group, _ = Group.objects.get_or_create(name="admin")
        target_user.groups.add(group)

        return Response({"message": f"{target_user.username} artık admin."}, status=status.HTTP_200_OK)
