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
	email = serializers.ReadOnlyField(source='user.email')

	class Meta:
		model = AppuntaTeacher
		fields = ('id', 'first_name', 'last_name', 'email')


class AppuntaTeacherSerializer(serializers.ModelSerializer):
	user = GenericUserSerializer(read_only=True)
	user_type = serializers.SerializerMethodField()

	class Meta:
		model = AppuntaTeacher
		fields = ('id', 'user', 'institution', 'rut', 'bio', 'user_type')

	def get_user_type(self, _):
		return 'teacher'


class AppuntaStudentSerializer(serializers.ModelSerializer):
	user = GenericUserSerializer(read_only=True)
	user_type = serializers.SerializerMethodField()

	class Meta:
		model = AppuntaStudent
		fields = ('id', 'user', 'institution', 'user_type')

	def get_user_type(self, _):
		return 'student'


class GenericUserRegisterSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('first_name', 'last_name', 'password', 'email')
		write_only_fields = ('first_name', 'last_name', 'password', 'email')

	def create(self, validated_data):
		validated_data['username'] = validated_data.get('email', None)
		return super(GenericUserRegisterSerializer, self).create(validated_data)


def create_user(validated_data):
	user_data = {k: validated_data[k] for k in ('first_name', 'last_name', 'email')}
	user_data['username'] = validated_data['email']
	user = User.objects.create(**user_data)
	user.set_password(validated_data['password'])
	user.save()
	return user


class AppuntaTeacherRegisterSerializer(serializers.ModelSerializer):
	user = GenericUserSerializer(read_only=True)
	first_name = serializers.CharField(write_only=True)
	last_name = serializers.CharField(write_only=True)
	password = serializers.CharField(write_only=True)
	email = serializers.CharField(write_only=True)

	class Meta:
		model = AppuntaTeacher
		fields = ('id', 'user', 'first_name', 'last_name', 'password', 'email',
		          'institution', 'birth_date', 'rut', 'bio')
		write_only_fields = ('institution', 'birth_date', 'rut', 'bio')
		read_only_fields = ('id', 'user')

	def create(self, validated_data):
		user = create_user(validated_data)
		teacher_data = {k: validated_data[k] for k in ('institution', 'birth_date', 'rut', 'bio')}
		teacher = AppuntaTeacher.objects.create(**teacher_data, user=user)
		return teacher


class AppuntaStudentRegisterSerializer(serializers.ModelSerializer):
	user = GenericUserSerializer(read_only=True)
	first_name = serializers.CharField(write_only=True)
	last_name = serializers.CharField(write_only=True)
	password = serializers.CharField(write_only=True)
	email = serializers.CharField(write_only=True)

	class Meta:
		model = AppuntaStudent
		fields = ('id', 'user', 'first_name', 'last_name', 'password', 'email',
		          'institution', 'birth_date')
		write_only_fields = ('institution', 'birth_date')
		read_only_fields = ('id', 'user')

	def create(self, validated_data):
		user = create_user(validated_data)
		student_data = {k: validated_data[k] for k in ('institution', 'birth_date')}
		student = AppuntaStudent.objects.create(**student_data, user=user)
		return student