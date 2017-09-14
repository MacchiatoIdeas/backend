from users.serializers import *
from .models import AutomatedExercise, check_right_answer_right


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
