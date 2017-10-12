from users.serializers import *
from .models import *

class AutomatedExerciseListSerializer(serializers.ModelSerializer):
	author = TeacherSerializer(read_only=True)

	class Meta:
		model = AutomatedExercise
		fields = ('id', 'difficulty', 'author', 'briefing', 'schema')


class AutomatedExerciseSerializer(serializers.ModelSerializer):
	author = TeacherSerializer(read_only=True)

	def validate(self, data):
		if not check_right_answer_right(data['content'], data['right_answer']):
			raise serializers.ValidationError("right_answer invalid with the content!")
		return data

	class Meta:
		model = AutomatedExercise
		fields = ('id', 'difficulty', 'author', 'unit', 'briefing', 'content', 'right_answer')

class AutomatedExerciseAnswerSerializer(serializers.ModelSerializer):
	user = GenericUserSerializer(read_only=True)
	score = serializers.ReadOnlyField(source="get_score")

	class Meta:
		model = AutomatedExerciseAnswer
		fields = ('user','exercise','answer','score')


class AutomatedExerciseSelectSerializer(serializers.ModelSerializer):
	class Meta:
		model = AutomatedExercise
		fields = ('id')


class ExerciseCommentSerializer(serializers.ModelSerializer):
	user = GenericUserSerializer(read_only=True)
	#exercise = AutomatedExerciseSerializer(read_only=True)
	#exercise_id = serializers.IntegerField(write_only=True)

	class Meta:
		model = ExerciseComment
		fields = '__all__'