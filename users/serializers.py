from django.contrib.auth.models import User, Group
from rest_framework import serializers

from .models import Teacher
from material.models import Guide, GuideItem, Content, Subject
from exercises.models import check_right_answer_right, AutomatedExercise


class UserAutomatedExerciseSerializer(serializers.ModelSerializer):
	def validate(self, data):
		if not check_right_answer_right(data['content'], data['right_answer']):
			raise serializers.ValidationError("right_answer invalid with the content!")
		return data

	class Meta:
		model = AutomatedExercise
		fields = ('id', 'difficulty', 'author', 'unit', 'briefing', 'content', 'right_answer')


class UserContentGuideSerializer(serializers.ModelSerializer):
	class Meta:
		model = Content
		fields = ('id', 'unit', 'subtitle', 'summary', 'text', 'html_text', 'author')


class UserGuideItemSerializer(serializers.ModelSerializer):
	type = serializers.SerializerMethodField()
	item = serializers.SerializerMethodField()

	class Meta:
		model = GuideItem
		fields = ('type', 'item')

	def get_type(self, gitem):
		if gitem.content is not None:
			return 'content'
		elif gitem.exercise is not None:
			return 'exercise'
		else:
			return 'unknown'

	def get_item(self, gitem):
		if gitem.content is not None:
			return UserContentGuideSerializer(instance=gitem.content).data
		elif gitem.exercise is not None:
			return UserAutomatedExerciseSerializer(instance=gitem.exercise).data
		else:
			return None


class UserSubjectSerializer(serializers.ModelSerializer):
	class Meta:
		model = Subject
		fields = ('id', 'name', 'color', 'thumbnail')


class UserGuidesSerializer(serializers.ModelSerializer):
	items = UserGuideItemSerializer(many=True, read_only=True)
	subject = UserSubjectSerializer(read_only=True)

	class Meta:
		model = Guide
		fields = ('id', 'user', 'title', 'brief', 'subject', 'items')


class SimpleUserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('id', 'username', 'first_name', 'last_name', 'email')

class GenericUserSerializer(serializers.ModelSerializer):
	guides = UserGuidesSerializer(read_only=True, many=True)

	class Meta:
		model = User
		fields = ('id', 'username', 'first_name', 'last_name', 'email', 'guides')
		read_only_fields = ('username', 'first_name', 'last_name', 'email')


class GroupSerializer(serializers.ModelSerializer):
	class Meta:
		model = Group


class TeacherSerializer(serializers.ModelSerializer):
	first_name = serializers.ReadOnlyField(source='user.first_name')
	last_name = serializers.ReadOnlyField(source='user.last_name')

	class Meta:
		model = Teacher
		fields = ('id', 'first_name', 'last_name')
