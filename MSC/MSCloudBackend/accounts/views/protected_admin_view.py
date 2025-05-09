from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts.permissions import IsInGroup

class AdminOnlyView(APIView):
    permission_classes = [IsInGroup("admin")]

    def get(self, request):
        return Response({"message": "Bu endpoint sadece adminler içindir."})
