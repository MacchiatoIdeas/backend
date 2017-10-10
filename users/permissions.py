from rest_framework import permissions


class AuthenticatedUserType(permissions.BasePermission):
	def __init__(self, type_attr):
		super(AuthenticatedUserType, self).__init__()
		self._type_attr = type_attr

	def has_permission(self, request, view):
		# Read permissions are allowed to any request,
		# so we'll always allow GET, HEAD or OPTIONS requests.
		if request.method in permissions.SAFE_METHODS:
			return True

		# User must be authenticated.
		if request.user.is_anonymous():
			return False

		# User must be type_user
		return hasattr(request.user, self._type_attr)


class AuthenticatedTeacher(AuthenticatedUserType):
	def __init__(self):
		super(AuthenticatedTeacher, self).__init__('teacher')


class AuthenticatedAppuntaAdmin(AuthenticatedUserType):
	def __init__(self):
		super(AuthenticatedAppuntaAdmin, self).__init__('appunta_admin')


class IsMemberOfCourse(permissions.BasePermission):
    # Only allow users related to the course.
    """
    Only members can do anything, and only the teacher can do unsafe things.
    """

    def has_object_permission(self, request, view, obj):
        is_safe = request.method in permissions.SAFE_METHODS
        participant = request.user in obj.participants.all()
        the_teacher = hasattr(request.user,'teacher') and (request.user.teacher == obj.teacher)
        return ((participant and is_safe) or the_teacher)
