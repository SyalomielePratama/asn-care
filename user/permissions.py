from rest_framework import permissions

class IsSuperUser(permissions.BasePermission):
    """
    Permission check for superusers.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser

class IsPegawai(permissions.BasePermission):
    """
    Permission check for pegawai users.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_pegawai

class IsPegawaiOrReadOnly(permissions.BasePermission):
    """
    Allows pegawai users to update their own profile, but read-only for others.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        return obj.email == request.user.email