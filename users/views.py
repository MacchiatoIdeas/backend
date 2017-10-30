from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope
from .serializers import *

from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework.generics import CreateAPIView


def get_serializer_class(user):
	if hasattr(user, 'teacher'):
		return AppuntaTeacherSerializer,  'teacher'
	elif hasattr(user, 'student'):
		return AppuntaStudentSerializer,  'student'
	else:
		return GenericUserSerializer,     'generic'


class GetMe(APIView):
	def get(self, request):
		SerializerClass, t = get_serializer_class(request.user)
		serializer = SerializerClass(getattr(request.user, t, request.user))
		return Response(serializer.data)


class UserViewSet(ModelViewSet):
	permission_classes = [IsAuthenticated, TokenHasReadWriteScope]
	queryset = User.objects.all()
	serializer_class = GenericUserSerializer

	def get_serializer_class(self):
		if hasattr(self._obj.user, 'teacher'):
			return AppuntaTeacherSerializer
		elif hasattr(self._obj.user, 'student'):
			return AppuntaStudentSerializer
		else:
			return super(UserViewSet, self).get_serializer_class()

	def get_queryset(self):
		user_id = self.kwargs.get('pk', None)

		if user_id is not None:
			user = User.objects.get(id=user_id)

			if hasattr(user, 'teacher'):
				self.kwargs['pk'] = user.teacher.id
				return AppuntaTeacher.objects.all()
			elif hasattr(user, 'student'):
				self.kwargs['pk'] = user.student.id
				return AppuntaStudent.objects.all()

		return super(UserViewSet, self).get_queryset()

	def get_object(self):
		obj = super(UserViewSet, self).get_object()
		self._obj = obj
		return obj


class AppuntaTeacherRegisterView(CreateAPIView):
	model = AppuntaTeacher
	serializer_class = AppuntaTeacherRegisterSerializer
	permission_classes = [AllowAny]


class AppuntaStudentRegisterView(CreateAPIView):
	model = AppuntaStudent
	serializer_class = AppuntaStudentRegisterSerializer
	permission_classes = [AllowAny]


class GroupViewSet(ModelViewSet):
	permission_classes = [IsAuthenticated, TokenHasScope]
	required_scopes = ['groups']
	queryset = Group.objects.all()
	serializer_class = GroupSerializer
