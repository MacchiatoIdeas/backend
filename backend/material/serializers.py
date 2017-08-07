from rest_framework import serializers

from users.serializers import TeacherSerializer
from .models import *


class SubUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubUnit
        fields = ('id', 'unit', 'name',)


class SubUnitListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubUnit
        fields = ('id', 'name',)


class UnitSerializer(serializers.ModelSerializer):
    sub_units = SubUnitListSerializer(many=True, read_only=True)

    class Meta:
        model = Unit
        fields = ('id', 'field_of_study', 'name', 'sub_units')


class UnitListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = ('id', 'name')


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
        fields = ('id', 'sub_unit', 'text', 'author')


class ContentListSerializer(serializers.ModelSerializer):
    text = serializers.ReadOnlyField(source='abstract')
    author = TeacherSerializer()

    class Meta:
        model = Content
        fields = ('id', 'text', 'author')


class SubUnitRetrieveSerializer(serializers.ModelSerializer):
    contents = ContentListSerializer(many=True)
    unit = UnitListSerializer()

    class Meta:
        model = SubUnit
        fields = ('id', 'unit', 'name', 'contents')


class ContentRetrieveSerializer(serializers.ModelSerializer):
    author = TeacherSerializer()
    sub_unit = SubUnitSerializer()

    class Meta:
        model = Content
        fields = ('id', 'sub_unit', 'text', 'author')
