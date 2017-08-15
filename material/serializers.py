from rest_framework import serializers

from users.serializers import *
from .models import *


class ContentListSerializer(serializers.ModelSerializer):
    text = serializers.ReadOnlyField(source='abstract')
    author = TeacherSerializer()

    class Meta:
        model = Content
        fields = ('id', 'unit', 'summary', 'text', 'html_text', 'author')


class UnitSerializer(serializers.ModelSerializer):
    contents = ContentListSerializer(many=True, read_only=True)

    class Meta:
        model = Unit
        fields = ('id', 'field_of_study', 'name', 'academic_level', 'contents')


class UnitListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = ('id', 'field_of_study', 'name')


class FieldOfStudySerializer(serializers.ModelSerializer):
    class Meta:
        model = FieldOfStudy
        fields = ('id', 'name')


class FieldOfStudyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = FieldOfStudy
        fields = ('id', 'name')


class FieldOfStudyRetrieveSerializer(serializers.ModelSerializer):
    units = UnitListSerializer(many=True, read_only=True)

    class Meta:
        model = FieldOfStudy
        fields = ('id', 'name', 'units')


class ContentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.user.username')
    # TODO: Change user name for the proper full name of a teacher.

    class Meta:
        model = Content
        fields = ('id', 'unit', 'subtitle', 'summary', 'text', 'html_text', 'author')


class ContentRetrieveSerializer(serializers.ModelSerializer):
    author = TeacherSerializer()
    unit = UnitSerializer()

    class Meta:
        model = Content
        fields = ('id', 'unit', 'subtitle', 'summary', 'text', 'html_text', 'author')


class CommentSerializer(serializers.ModelSerializer):
    user = GenericUserSerializer(read_only=True)
    # TODO: Should the content be retrieved?
    #content = ContentSerializer()

    class Meta:
        model = Comment
        fields = '__all__'


class FeedbackCommentSerializer(serializers.ModelSerializer):
    user = GenericUserSerializer(read_only=True)

    class Meta:
        model = FeedbackComment
        fields = '__all__'
