from django.contrib.auth.models import User, Group
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope
from .serializers import GenericUserSerializer, GroupSerializer, CourseSerializer
from .permissions import AuthenticatedTeacher,IsMemberOfCourse
from .models import Course


class UserViewSet(ModelViewSet):
	permission_classes = [IsAuthenticated, TokenHasReadWriteScope]
	queryset = User.objects.all()
	serializer_class = GenericUserSerializer


class GroupViewSet(ModelViewSet):
	permission_classes = [IsAuthenticated, TokenHasScope]
	required_scopes = ['groups']
	queryset = Group.objects.all()
	serializer_class = GroupSerializer

class CourseViewSet(ModelViewSet):
	permission_classes = [AuthenticatedTeacher,IsMemberOfCourse]
	serializer_class = CourseSerializer
	queryset = Course.objects.all()

	def get_queryset(self):
		if hasattr(self.request.user,'teacher'):
			return Course.objects.filter(teacher=self.request.user.teacher)
		else:
			return None

	def perform_create(self, serializer):
		serializer.save(teacher=self.request.user.teacher)
