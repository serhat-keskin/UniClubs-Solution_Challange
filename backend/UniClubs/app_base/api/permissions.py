from rest_framework import permissions
from pprint import pprint

# class IsAdminUserOrReadOnly(permissions.BasePermission):
#     def has_permission(self, request, view):
#         return bool(request.method in permissions.SAFE_METHODS or 
#         request.user and request.user.is_staff)

class IsAdminUserOrReadOnly(permissions.IsAdminUser):
    def has_permission(self, request, view):
        is_admin = super().has_permission(request, view)
        return is_admin or request.method in permissions.SAFE_METHODS
# pprint(dir(permissions))


class IsYorumSahibiOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(request.method in permissions.SAFE_METHODS or request.user == obj.yorum_sahibi)