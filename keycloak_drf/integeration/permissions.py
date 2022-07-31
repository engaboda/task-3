from rest_framework.permissions import BasePermission


class IsAdminUser(BasePermission):
    """
        Allows access only to Admin Api if user is Admin
    """

    def has_permission(self, request, view):
        if request.user.role == 'admin':
            return True
        return False


class IsNormalUser(BasePermission):
    """
        Allows access only to normal Api if user is normal
    """

    def has_permission(self, request, view):
        if request.user.role == 'normal':
            return True
        return False
