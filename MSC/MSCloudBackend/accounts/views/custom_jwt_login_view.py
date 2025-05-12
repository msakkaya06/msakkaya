from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import update_last_login
from rest_framework.response import Response
from rest_framework import status

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({"error": "Giriş başarısız"}, status=status.HTTP_401_UNAUTHORIZED)

        user = serializer.user

        if not user.is_active:
            return Response({"error": "Bu kullanıcı pasif durumda"}, status=status.HTTP_403_FORBIDDEN)

        update_last_login(None, user)

        return Response(serializer.validated_data, status=status.HTTP_200_OK)
