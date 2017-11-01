from rest_framework import serializers

from .models import *
from exercises.models import AutomatedExerciseAnswer

from users.serializers import TeacherSerializer, AppuntaStudentSerializer, AppuntaTeacherSerializer
from material.serializers import GuideSerializer,GuideListSerializer
from exercises.serializers import AutomatedExerciseAnswerSerializer


class CourseSerializer(serializers.ModelSerializer):
	teacher = TeacherSerializer(read_only=True)
	participants = AppuntaStudentSerializer(read_only=True, many=True)

	class Meta:
		model = Course
		fields = ('id', 'name','teacher', 'participants')


class EachLinkSerializer(serializers.ModelSerializer):
	guide = GuideSerializer()
	answers = AutomatedExerciseAnswerSerializer(source='get_answers', many=True)

	class Meta:
		model = CourseLink
		fields = ('guide', 'answers')

	def get_answers(self, course_link):
		query = AutomatedExerciseAnswer.objects\
			.filter(user__student__course=course_link.course)\
			.filter(exercise__guideitem__guide=course_link.guide)
		return AutomatedExerciseAnswerSerializer(query, many=True).data


class CourseWithGuidesSerializer(serializers.ModelSerializer):
	teacher = AppuntaTeacherSerializer(read_only=True)
	participants = AppuntaStudentSerializer(read_only=True, many=True)
	guides = serializers.SerializerMethodField()

	class Meta:
		model = Course
		fields = ('id', 'name','teacher', 'participants', 'guides')

	def get_guides(self, course):
		query = CourseLink.objects.filter(course=course)
		return EachLinkSerializer(query, many=True).data


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
