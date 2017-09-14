from rest_framework import serializers

from users.serializers import *
from exercises.serializers import AutomatedExerciseListSerializer
from .models import *


class ContentListSerializer(serializers.ModelSerializer):
	text = serializers.ReadOnlyField(source='abstract')
	author = TeacherSerializer(read_only=True)

	class Meta:
		model = Content
		fields = ('id', 'unit', 'summary', 'text', 'html_text', 'author')


class SubjectSerializer(serializers.ModelSerializer):
	class Meta:
		model = Subject
		fields = ('id', 'name', 'color', 'thumbnail')


class SubjectListSerializer(serializers.ModelSerializer):
	class Meta:
		model = Subject
		fields = ('id', 'name', 'color', 'thumbnail')


class UnitSerializer(serializers.ModelSerializer):
	contents = ContentListSerializer(many=True, read_only=True)
	exercises = AutomatedExerciseListSerializer(many=True, read_only=True)
	subject = SubjectSerializer(read_only=True)

	class Meta:
		model = Unit
		fields = ('id', 'subject', 'name', 'academic_level', 'contents', 'exercises')

class UnitListSerializer(serializers.ModelSerializer):
	class Meta:
		model = Unit
		fields = ('id', 'subject', 'name', 'academic_level')


class SubjectRetrieveSerializer(serializers.ModelSerializer):
	units = UnitListSerializer(many=True, read_only=True)

	class Meta:
		model = Subject
		fields = ('id', 'name', 'units', 'color', 'thumbnail')


class ContentSerializer(serializers.ModelSerializer):
	author = TeacherSerializer(read_only=True)

	class Meta:
		model = Content
		fields = ('id', 'unit', 'subtitle', 'summary', 'text', 'html_text', 'author')


class ContentRetrieveSerializer(serializers.ModelSerializer):
	author = TeacherSerializer(read_only=True)
	unit = UnitSerializer()

	class Meta:
		model = Content
		fields = ('id', 'unit', 'subtitle', 'summary', 'text', 'html_text', 'author')


class CommentSerializer(serializers.ModelSerializer):
	user = GenericUserSerializer(read_only=True)

	# TODO: Should the content be retrieved?
	# content = ContentSerializer()

	class Meta:
		model = Comment
		fields = '__all__'


class FeedbackCommentSerializer(serializers.ModelSerializer):
	user = GenericUserSerializer(read_only=True)

	class Meta:
		model = FeedbackComment
		fields = '__all__'
