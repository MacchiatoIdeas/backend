from rest_framework import serializers

from users.serializers import *
from .models import *
from material.models import Subject,Unit


# NOTE: <distemper>
class SubjectSerializer2(serializers.ModelSerializer):
	class Meta:
		model = Subject
		fields = ('id', 'name', 'color', 'thumbnail')
class UnitWithSubjectRetrieveSerializer2(serializers.ModelSerializer):
	subject = SubjectSerializer2(read_only=True)
	class Meta:
		model = Unit
		fields = ('id', 'subject', 'name', 'academic_level')
# </distemper>

class ExerciseCommentSerializer(serializers.ModelSerializer):
	user = GenericUserSerializer(read_only=True)
	#exercise = AutomatedExerciseSerializer(read_only=True)
	#exercise_id = serializers.IntegerField(write_only=True)

	class Meta:
		model = ExerciseComment
		fields = '__all__'

class AutomatedExerciseListSerializer(serializers.ModelSerializer):
	author = TeacherSerializer(read_only=True)
	comment_count = serializers.SerializerMethodField()

	class Meta:
		model = AutomatedExercise
		fields = ('id', 'difficulty', 'author',
		          'briefing', 'schema', 'moment',
		          'comment_count')

	def get_comment_count(self, ex):
		return ExerciseComment.objects.filter(exercise=ex).count()


class AutomatedExerciseSerializer(serializers.ModelSerializer):
	author = TeacherSerializer(read_only=True)
	comments = ExerciseCommentSerializer(many=True, read_only=True)

	def validate(self, data):
		if not check_right_answer_right(data['content'], data['right_answer']):
			raise serializers.ValidationError("right_answer invalid with the content!")
		return data

	class Meta:
		many = True
		model = AutomatedExercise
		fields = ('id', 'difficulty', 'author', 'unit', 'briefing', 'content', 'right_answer', 'comments','text','moment')

class AutomatedExerciseRetrieveSerializer(AutomatedExerciseSerializer):
	unit = UnitWithSubjectRetrieveSerializer2()

class AutomatedExerciseAnswerInputSerializer(serializers.ModelSerializer):
	class Meta:
		model = AutomatedExerciseAnswer
		fields = ('id','exercise','answer')


class AutomatedExerciseAnswerSerializer(serializers.ModelSerializer):
	student = AppuntaStudentSerializer(read_only=True)
	score = serializers.ReadOnlyField(source="get_score")
	exercise = AutomatedExerciseListSerializer(read_only=True)

	class Meta:
		model = AutomatedExerciseAnswer
		fields = ('id','student','exercise','answer','score','tscore','moment')


class AutomatedExerciseSelectSerializer(serializers.ModelSerializer):
	class Meta:
		model = AutomatedExercise
		fields = ('id')
