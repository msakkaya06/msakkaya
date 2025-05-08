from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth import authenticate
from accounts.serializers.password_serializers import ChangePasswordSerializer
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken


class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        old_password = serializer.validated_data["old_password"]
        new_password = serializer.validated_data["new_password"]

        if not user.check_password(old_password):
            return Response({"error": "Eski şifre yanlış"}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()

        # Tüm refresh token'ları iptal et
        tokens = OutstandingToken.objects.filter(user=user)
        for token in tokens:
            try:
                BlacklistedToken.objects.get_or_create(token=token)
            except:
                pass

        return Response({"message": "Şifre başarıyla değiştirildi"}, status=status.HTTP_200_OK)
