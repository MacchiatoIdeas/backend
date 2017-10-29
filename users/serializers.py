from django.contrib.auth.models import User, Group
from rest_framework import serializers

from .models import *


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


class AppuntaTeacherSerializer(serializers.ModelSerializer):
	first_name = serializers.ReadOnlyField(source='user.first_name')
	last_name = serializers.ReadOnlyField(source='user.last_name')
	user_type = serializers.SerializerMethodField()

	class Meta:
		model = AppuntaTeacher
		fields = ('id', 'first_name',
		          'last_name', 'institution', 'rut', 'bio', 'user_type')

	def get_user_type(self, _):
		return 'teacher'


class AppuntaStudentSerializer(serializers.ModelSerializer):
	first_name = serializers.ReadOnlyField(source='user.first_name')
	last_name = serializers.ReadOnlyField(source='user.last_name')
	user_type = serializers.SerializerMethodField()

	class Meta:
		model = AppuntaStudent
		fields = ('id', 'first_name', 'last_name', 'institution', 'user_type')

	def get_user_type(self, _):
		return 'student'


class AppuntaTeacherRegisterSerializer(serializers.ModelSerializer):
	first_name = serializers.CharField(source='user.first_name')
	last_name = serializers.CharField(source='user.last_name')
	email = serializers.CharField(source='user.email')
	password = serializers.CharField(source='user.password', write_only=True)

	class Meta:
		model = AppuntaTeacher
		fields = ('id', 'first_name', 'last_name', 'password', 'email',
		          'institution', 'birth_date', 'rut', 'bio')
		write_only_fields = ('password',)

	def create(self, validated_data):
		if validated_data.get('password', None) == None:
			raise AttributeError('Password cannot be null')

		user = User.objects.create(**validated_data)
		user.set_password(validated_data['password'])

		teacher = AppuntaTeacher.objects.create(**validated_data, user=user)
		return teacher