from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    """
    본인의 data만 접근 가능
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user