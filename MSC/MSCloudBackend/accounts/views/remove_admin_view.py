from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth.models import Group
from accounts.models import CustomUser

class RemoveAdminView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user_id = request.data.get("user_id")
        if not user_id:
            return Response({"error": "Kullanıcı ID gerekli"}, status=400)

        try:
            user = CustomUser.objects.get(id=user_id)
            admin_group = Group.objects.get(name="admin")
            user.groups.remove(admin_group)
            return Response({"message": "Admin yetkisi kaldırıldı"}, status=200)
        except CustomUser.DoesNotExist:
            return Response({"error": "Kullanıcı bulunamadı"}, status=404)
        except Group.DoesNotExist:
            return Response({"error": "Admin grubu yok"}, status=500)
