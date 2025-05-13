from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from accounts.models import CustomUser
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from msc_core.messages.accounts import ACCOUNT_MESSAGES  # ✅

def blacklist_user_tokens(user):
    tokens = OutstandingToken.objects.filter(user=user)
    for token in tokens:
        BlacklistedToken.objects.get_or_create(token=token)

class ToggleActiveView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user_id = request.data.get("user_id")
        if not user_id:
            return Response({"error": ACCOUNT_MESSAGES["user_id_required"]}, status=400)

        try:
            user = CustomUser.objects.get(id=user_id)
            user.is_active = not user.is_active
            if not user.is_active:
                blacklist_user_tokens(user)
            user.save()

            status_msg = ACCOUNT_MESSAGES["user_disabled"] if not user.is_active else ACCOUNT_MESSAGES["user_enabled"]

            return Response({"message": f"{user.username} - {status_msg}"}, status=200)

        except CustomUser.DoesNotExist:
            return Response({"error": ACCOUNT_MESSAGES["user_not_found"]}, status=404)
