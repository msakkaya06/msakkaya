from rest_framework import permissions

def IsInGroup(group_name):
    class _IsInGroup(permissions.BasePermission):
        def has_permission(self, request, view):
            return (
                request.user
                and request.user.is_authenticated
                and request.user.groups.filter(name=group_name).exists()
            )
    return _IsInGroup