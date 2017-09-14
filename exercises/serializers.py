from rest_framework import serializers

from users.serializers import *
from .models import AutomatedExercise,check_right_answer_right

class AutomatedExerciseListSerializer(serializers.ModelSerializer):
    #schema = serializers.ReadOnlyField(source='schema')
    author = serializers.ReadOnlyField(source='author.user.username')

    class Meta:
        model = AutomatedExercise
        fields = ('id', 'difficulty', 'author', 'briefing', 'schema')

class AutomatedExerciseSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.user.username')
    # TODO: Change user name for the proper full name of a teacher.

    def validate(self, data):
        if not check_right_answer_right(data['content'],data['right_answer']):
            raise serializers.ValidationError("right_answer invalid with the content!")
        return data

    class Meta:
        model = AutomatedExercise
        fields = ('id', 'difficulty', 'author', 'unit', 'briefing', 'content', 'right_answer')
