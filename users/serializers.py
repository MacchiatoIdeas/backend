from django.contrib.auth.models import User, Group
from rest_framework import serializers

from .models import AppuntaTeacher
from material.models import Guide, GuideItem, Content, Subject
from exercises.models import check_right_answer_right, AutomatedExercise



class GenericUserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('id', 'username', 'first_name', 'last_name', 'email')
		read_only_fields = ('username', 'first_name', 'last_name', 'email')


class GroupSerializer(serializers.ModelSerializer):
	class Meta:
		model = Group


class TeacherSerializer(serializers.ModelSerializer):
	first_name = serializers.ReadOnlyField(source='user.first_name')
	last_name = serializers.ReadOnlyField(source='user.last_name')

	class Meta:
		model = AppuntaTeacher
		fields = ('id', 'first_name', 'last_name')
