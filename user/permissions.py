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

class IsSuperUserOrReadOnly(permissions.BasePermission):
    """
    Allows read access to any authenticated user, but write access only to superusers.
    """
    def has_permission(self, request, view):
        # Allow read access to all authenticated users
        if request.method in permissions.SAFE_METHODS and request.user and request.user.is_authenticated:
            return True
        # Allow write access only to superusers
        return request.user and request.user.is_superuser

class IsSuperUserOrOwnProfile(permissions.BasePermission):
    """
    Allows read and update access to own profile, but full access only to superusers.
    """
    def has_object_permission(self, request, view, obj):
        # Superusers have full access
        if request.user and request.user.is_superuser:
            return True

        # Authenticated users can view their own profile
        if request.method in permissions.SAFE_METHODS and request.user and request.user.is_authenticated:
            try:
                pegawai = obj.pegawai_set.first() # Assuming reverse relation from User to Pegawai
                return pegawai.email == request.user.email
            except AttributeError:
                # Handle cases where the object might not have a direct pegawai relation
                # You might need to adjust this based on your model structure
                return False

        # Authenticated users can update their own profile
        if request.method in ['PUT', 'PATCH'] and request.user and request.user.is_authenticated:
            try:
                pegawai = obj.pegawai_set.first() # Assuming reverse relation from User to Pegawai
                return pegawai.email == request.user.email
            except AttributeError:
                return False

        return False