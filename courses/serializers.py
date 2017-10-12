from rest_framework import serializers

from .models import *

from users.serializers import TeacherSerializer


class CourseSerializer(serializers.ModelSerializer):
	teacher = TeacherSerializer(read_only=True)

	class Meta:
		model = Course
		fields = ('name','teacher', 'participants')

class CourseLinkInputSerializer(serializers.ModelSerializer):
	course = CourseSerializer()

	class Meta:
		model = CourseLink
		fields = ('course','guide')
