from rest_framework.viewsets import ModelViewSet
from rest_framework.mixins import CreateModelMixin
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope
from .serializers import *

from rest_framework.response import Response
from rest_framework.views import APIView


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
	permission_classes = [IsAuthenticated,TokenHasReadWriteScope]
	queryset = User.objects.all()

	def get_serializer_class(self):
		SerializerClass, _ = get_serializer_class(self.request.user)
		return SerializerClass

	def get_queryset(self):
		_, t = get_serializer_class(self.request.user)
		if t == 'teacher':
			return AppuntaTeacher.objects.all()
		elif t == 'student':
			return AppuntaStudent.objects.all()
		else:
			return User.objects.all()


class AppuntaTeacherRegisterView(CreateModelMixin, GenericAPIView):
	queryset = AppuntaTeacher.objects.all()
	serializer_class = AppuntaTeacherRegisterSerializer
	permission_classes = [AllowAny]


class GroupViewSet(ModelViewSet):
	permission_classes = [IsAuthenticated, TokenHasScope]
	required_scopes = ['groups']
	queryset = Group.objects.all()
	serializer_class = GroupSerializer
