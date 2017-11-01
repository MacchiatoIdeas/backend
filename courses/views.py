from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet

from users.permissions import AuthenticatedTeacher

from rest_framework import permissions

from .serializers import *

class CourseViewSet(ModelViewSet):
	permission_classes = [AuthenticatedTeacher,permissions.IsAuthenticated]
	serializer_class = CourseSerializer
	queryset = Course.objects.all()

	def get_queryset(self):
		if hasattr(self.request.user, 'teacher'):
			return Course.objects.filter(teacher=self.request.user.teacher)
		elif hasattr(self.request.user, 'student'):
			return Course.objects.filter(participants=self.request.user.student)
		else:
			return Course.objects.filter(participants=self.request.user)

	def get_serializer_class(self):
		if self.action in ('retrieve',):
			return CourseWithGuidesSerializer
		return super(CourseViewSet, self).get_serializer_class()

	def perform_create(self, serializer):
		serializer.save(teacher=self.request.user.teacher)

class CourseLinkViewSet(ModelViewSet):
	permission_classes = [AuthenticatedTeacher]
	serializer_class = CourseLinkSerializer
	queryset = CourseLink.objects.all()

	def get_queryset(self):
		if (hasattr(self.request.user, 'teacher')):
			return CourseLink.objects.filter(
				course__teacher=self.request.user.teacher)
		elif hasattr(self.request.user, 'student'):
			return CourseLink.objects.filter(
				course__participants=self.request.user.student)
		else:
			return CourseLink.objects.filter(
				course__participants=self.request.user)

	def get_serializer_class(self):
		if self.action in ('create',):
			return CourseLinkInputSerializer
		return super().get_serializer_class()
