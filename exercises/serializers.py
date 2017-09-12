from rest_framework import serializers

from users.serializers import *
from .models import AutomatedExercise

class AutomatedExerciseSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.user.username')
    # TODO: Change user name for the proper full name of a teacher.

    class Meta:
        model = AutomatedExercise
        fields = ('id', 'author', 'briefing', 'content', 'right_answer')
