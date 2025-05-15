from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from accounts.models import CustomUser
from accounts.permissions import IsInGroup
from accounts.serializers.user_serializer import UserSerializer
class AdminUserListView(APIView):
    permission_classes = [IsInGroup("admin")]

    def get(self, request):
        users = CustomUser.objects.all()

        # 🔍 Arama filtresi en başta
        search = request.query_params.get("search")
        if search:
            users = users.filter(
                Q(email__icontains=search) |
                Q(username__icontains=search) |
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search)
            )

        # 🟢 Aktif / Pasif filtresi
        is_active = request.query_params.get("is_active")
        if is_active == "true":
            users = users.filter(is_active=True)
        elif is_active == "false":
            users = users.filter(is_active=False)

        # 🟣 Admin grubu filtresi
        is_admin = request.query_params.get("is_admin")
        if is_admin == "true":
            users = users.filter(groups__name="admin")
        elif is_admin == "false":
            users = users.exclude(groups__name="admin")

        # 🔽 Sıralama (en yeni en üstte)
        users = users.order_by("id")

        # 📄 Sayfalama
        paginator = PageNumberPagination()
        paginator.page_size = 10
        result_page = paginator.paginate_queryset(users, request)

        # 🔄 Serialize
        serializer = UserSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)