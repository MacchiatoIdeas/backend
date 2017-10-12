from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet

from users.permissions import AuthenticatedTeacher

from .serializers import *

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
