from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.pagination import PageNumberPagination

from accounts.models import CustomUser
from accounts.permissions import IsInGroup
from accounts.serializers.user_serializer import UserSerializer

class AdminUserListView(APIView):
    permission_classes = [IsInGroup("admin")]

    def get(self, request):
        users = CustomUser.objects.all().order_by("id")

    # filtre ekle
        is_active = request.query_params.get("is_active")
        if is_active == "true":
            users = users.filter(is_active=True)
        elif is_active == "false":
            users = users.filter(is_active=False)
        is_admin = request.query_params.get("is_admin")
        if is_admin == "true":
            users = users.filter(groups__name="admin")
        elif is_admin == "false":
            users = users.exclude(groups__name="admin")

        paginator = PageNumberPagination()
        paginator.page_size = 10
        result_page = paginator.paginate_queryset(users, request)

        serializer = UserSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)