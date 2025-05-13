from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts.serializers.register_serializers import RegisterSerializer
from accounts.services.user_service import UserService
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from msc_core.messages.accounts import ACCOUNT_MESSAGES  # ✅ eklendi

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = UserService.create_user(
            username=serializer.validated_data["username"],
            email=serializer.validated_data["email"],
            password=serializer.validated_data["password"],
            first_name=serializer.validated_data.get("first_name", ""),
            last_name=serializer.validated_data.get("last_name", "")
        )

        refresh = RefreshToken.for_user(user)

        return Response({
            "message": ACCOUNT_MESSAGES["user_created"],
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }, status=status.HTTP_201_CREATED)
