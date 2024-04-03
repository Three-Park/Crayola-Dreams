from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    """
    본인의 data만 접근 가능
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
    

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    객체를 만든 사용자만 수정할 수 있는 권한.
    """

    def has_object_permission(self, request, view, obj):
        # 읽기 권한은 항상 허용함
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True

        # 요청한 사용자가 해당 객체의 소유자인 경우에만 쓰기 권한을 부여함
        return obj.follower == request.user or obj.following_user == request.user