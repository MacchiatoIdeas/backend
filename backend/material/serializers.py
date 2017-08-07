from rest_framework import serializers
from .models import *

from users.serializers import TeacherSerializer


class SubUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubUnit
        fields = ('id', 'unit', 'name',)


class ContentSerializer(serializers.ModelSerializer):
    author = TeacherSerializer()
    sub_unit = SubUnitSerializer()

    class Meta:
        model = Content
        fields = ('id', 'sub_unit', 'text', 'author')


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
