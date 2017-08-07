from rest_framework import serializers

from users.serializers import TeacherSerializer
from .models import *


class SubUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubUnit
        fields = ('id', 'unit', 'name',)


class UnitSerializer(serializers.ModelSerializer):
    sub_units = SubUnitSerializer(many=True, read_only=True)

    class Meta:
        model = Unit
        fields = ('id', 'area', 'name', 'sub_units')


class FieldOfStudySerializer(serializers.ModelSerializer):
    units = UnitSerializer(many=True, read_only=True)

    class Meta:
        model = FieldOfStudy
        fields = ('id', 'name', 'units')


class ContentSerializer(serializers.ModelSerializer):
    # TODO: Change user name for the proper full name of a teacher.
    author = serializers.ReadOnlyField(source='author.user.full_name')

    class Meta:
        model = Content
        fields = ('id', 'sub_unit', 'text', 'author')


class ContentListSerializer(serializers.ModelSerializer):
    text = serializers.ReadOnlyField(source='abstract')
    author = TeacherSerializer()
    sub_unit = SubUnitSerializer()

    class Meta:
        model = Content
        fields = ('id', 'sub_unit', 'text', 'author')


class ContentRetrieveSerializer(serializers.ModelSerializer):
    author = TeacherSerializer()
    sub_unit = SubUnitSerializer()

    class Meta:
        model = Content
        fields = ('id', 'sub_unit', 'text', 'author')
