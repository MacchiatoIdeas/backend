from rest_framework import viewsets

from users.permissions import *
from .serializers import *


class AutomatedExerciseViewSet(viewsets.ModelViewSet):
    queryset = AutomatedExercise.objects.all()
    serializer_class = AutomatedExerciseSerializer

    permission_classes = (AuthenticatedTeacher,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user.teacher)

class AutomatedExerciseAnswerViewSet(viewsets.ModelViewSet):
    queryset = AutomatedExerciseAnswer.objects.all()
    serializer_class = AutomatedExerciseAnswerSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
