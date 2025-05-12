from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from accounts.models import CustomUser
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken

def blacklist_user_tokens(user):
        tokens = OutstandingToken.objects.filter(user=user)
        for token in tokens:
            BlacklistedToken.objects.get_or_create(token=token)
class ToggleActiveView(APIView):
    permission_classes = [permissions.IsAuthenticated]


    def post(self, request):
        user_id = request.data.get("user_id")
        if not user_id:
            return Response({"error": "Kullanıcı ID gerekli"}, status=400)

        try:
            user = CustomUser.objects.get(id=user_id)
            user.is_active = not user.is_active
            if not user.is_active:
                blacklist_user_tokens(user)
            user.save()
            return Response({"message": "Kullanıcı durumu güncellendi"}, status=200)
        except CustomUser.DoesNotExist:
            return Response({"error": "Kullanıcı bulunamadı"}, status=404)
