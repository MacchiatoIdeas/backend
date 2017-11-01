from rest_framework import serializers

from .models import *
from exercises.models import AutomatedExerciseAnswer

from users.serializers import TeacherSerializer, AppuntaStudentSerializer
from material.serializers import GuideSerializer,GuideListSerializer
from exercises.serializers import AutomatedExerciseAnswerSerializer


class CourseSerializer(serializers.ModelSerializer):
	teacher = TeacherSerializer(read_only=True)
	participants = AppuntaStudentSerializer(read_only=True, many=True)

	class Meta:
		model = Course
		fields = ('name','teacher', 'participants')

class CourseLinkOnCourseSerializer(serializers.ModelSerializer):
	guides = GuideListSerializer(many=True)

	class Meta:
		model = CourseLink
		fields = ('id','guide')

class CourseLinkSerializer(serializers.ModelSerializer):
	course = CourseSerializer()
	guide = GuideSerializer()
	answers = AutomatedExerciseAnswerSerializer(source='get_answers',many=True)

	class Meta:
		model = CourseLink
		fields = ('id','course','guide','answers')

class CourseLinkInputSerializer(serializers.ModelSerializer):
	class Meta:
		model = CourseLink
		fields = ('id','course','guide')
