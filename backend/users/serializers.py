from rest_framework import serializers

from users.models import Teacher


class TeacherSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)

    class Meta:
        model = Teacher
        fields = ('id', 'first_name', 'last_name')
