from rest_framework import serializers

from users.models import Teacher


class TeacherSerializer(serializers.ModelSerializer):
    first_name = serializers.ReadOnlyField(source='user.first_name')
    last_name = serializers.ReadOnlyField(source='user.last_name')

    class Meta:
        model = Teacher
        fields = ('id', 'first_name', 'last_name')
