from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth.models import Group
from accounts.models import CustomUser
from msc_core.messages.accounts import ACCOUNT_MESSAGES  

class RemoveAdminView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user_id = request.data.get("user_id")
        if not user_id:
            return Response({"error": ACCOUNT_MESSAGES["user_id_required"]}, status=400)

        try:
            user = CustomUser.objects.get(id=user_id)
            admin_group = Group.objects.get(name="admin")
            user.groups.remove(admin_group)

            return Response({
                "message": f"{user.username} - {ACCOUNT_MESSAGES['admin_removed']}"
            }, status=200)

        except CustomUser.DoesNotExist:
            return Response({"error": ACCOUNT_MESSAGES["user_not_found"]}, status=404)

        except Group.DoesNotExist:
            return Response({"error": ACCOUNT_MESSAGES["admin_group_missing"]}, status=500)
