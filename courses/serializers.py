from rest_framework import serializers

from .models import *
from exercises.models import AutomatedExerciseAnswer

from users.models import AppuntaStudent

from users.serializers import TeacherSerializer
from material.serializers import GuideSerializer,GuideListSerializer
from exercises.serializers import AutomatedExerciseAnswerSerializer


class EmailsSerializer(serializers.CharField):
	def to_representation(self, obj):
		prtcps = obj.all()
		return ",".join([x.user.email for x in prtcps])

	def to_internal_value(self, data):
		partis = []
		for em in data.split(','):
			query = AppuntaStudent.objects.filter(user__email=em)
			if query.count() > 0:
				partis.append(query.get())
		return partis


class CourseInputSerializer(serializers.ModelSerializer):
	participants = EmailsSerializer(allow_blank=True)

	class Meta:
		model = Course
		fields = ('name','participants')

class CourseSerializer(serializers.ModelSerializer):
	teacher = TeacherSerializer(read_only=True)

	class Meta:
		model = Course
		fields = ("id",'name','teacher','participants')

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
