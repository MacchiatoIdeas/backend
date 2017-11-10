from rest_framework import permissions

from .models import *

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

class AutomatedExerciseAnswerPermission(permissions.BasePermission):
	"""
	Only teachers can modify.
	Only student can create.
	"""
	def __init__(self):
		super(AutomatedExerciseAnswerPermission, self).__init__()

	def has_permission(self, request, view):
		if request.user.is_anonymous():
			return False
		if request.method in ('CREATE'):
			return hasattr(request.user, 'student')
		if request.method in ('PUT','PATCH'):
			return hasattr(request.user, 'teacher')
		return True

	def has_object_permission(self,request,view,obj):
		if request.user.is_anonymous():
			return False
		return (hasattr(request.user, 'teacher') or (hasattr(request.user, 'student') and request.user.student == obj.student))


class AuthenticatedTeacher(AuthenticatedUserType):
	"""
	Anyone can do safe things.
	Only teachers can do the other things.
	"""
	def __init__(self):
		super(AuthenticatedTeacher, self).__init__('teacher')


class AuthenticatedAppuntaAdmin(AuthenticatedUserType):
	"""
	Anyone can do safe things.
	Only admins can do the other things.
	"""
	def __init__(self):
		super(AuthenticatedAppuntaAdmin, self).__init__('appunta_admin')


class AuthenticatedAppuntaUser(permissions.BasePermission):
	"""
	Anyone can do safe things.
	Only teachers and students can do other things.
	"""

	def has_permission(self, request, view):
		if request.method in permissions.SAFE_METHODS:
			return True

		if request.user.is_anonymous():
			return False

		return hasattr(request.user, 'teacher') or hasattr(request.user, 'student')


class IsMemberOfCourse(permissions.BasePermission):
	"""
	Only members can do anything, and only the teacher can do unsafe things.
	"""

	def has_object_permission(self, request, view, obj):
		# NOTE: Ugly way of swap to the course if it is not one.
		if not hasattr(obj,'teacher'):
			obj = obj.course

		is_safe = request.method in permissions.SAFE_METHODS
		participant = hasattr(request.user,'student') and request.user.student in obj.participants.all()
		the_teacher = hasattr(request.user,'teacher') and (request.user.teacher == obj.teacher)
		return ((participant and is_safe) or the_teacher)


class IsAuthor(permissions.BasePermission):
	"""
	Only the author can do unsafe things.
	"""
	def has_object_permission(self, request, view, obj):
		if not hasattr(obj,'author'):
			obj = obj.guide
		if request.method in permissions.SAFE_METHODS:
			return True
		if request.user.is_anonymous():
			return False
		if hasattr(request.user,'teacher') and obj.author==request.user.teacher:
			return True
		return False

class NotPrivateOrRelated(permissions.BasePermission):
	"""
	If the object is private, only author teacher or students that are on a course with a courselink to that guide can do anything.
	"""

	def has_object_permission(self, request, view, obj):
		print("called on %s"%str(obj))
		if not hasattr(obj,'author'):
			obj = obj.guide
		return obj.not_priv_or_related(request.user)
