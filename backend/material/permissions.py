from rest_framework import permissions

from users.models import Teacher


class AuthenticatedTeacher(permissions.BasePermission):
    """
    Custom permission to only allow teachers.
    """

    def has_permission(self, request, view):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        # User must be authenticated.
        if request.user.is_anonymous():
            return False
        # User must have a teacher.
        try:
            teacher = request.user.teacher
            return True
        except Teacher.DoesNotExist:
            return False
