from django.contrib.auth.models import User, Group
from rest_framework import mixins
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope
from .serializers import *
from .permissions import AuthenticatedTeacher,IsMemberOfCourse
from .models import *


class UserViewSet(ModelViewSet):
	permission_classes = [IsAuthenticated],# TokenHasReadWriteScope]
	queryset = User.objects.all()
	serializer_class = GenericUserSerializer


class GroupViewSet(ModelViewSet):
	permission_classes = [IsAuthenticated]#, TokenHasScope]
	required_scopes = ['groups']
	queryset = Group.objects.all()
	serializer_class = GroupSerializer

class CourseViewSet(ModelViewSet):
	permission_classes = [AuthenticatedTeacher]
	serializer_class = CourseSerializer
	queryset = Course.objects.all()

	def get_queryset(self):
		if hasattr(self.request.user,'teacher'):
			return Course.objects.filter(teacher=self.request.user.teacher)
		else:
			return Course.objects.filter(participants=self.request.user)

	def perform_create(self, serializer):
		serializer.save(teacher=self.request.user.teacher)

class CourseLinkViewSet(ModelViewSet):
	permission_classes = [AuthenticatedTeacher]
	serializer_class = CourseLinkInputSerializer
	queryset = CourseLink.objects.all()

	def get_queryset(self):
		if (hasattr(self.request.user,"teacher")):
			return CourseLink.objects.filter(
				course__teacher=self.request.user.teacher)
		else:
			return CourseLink.objects.filter(
				course__participants=self.request.user)
