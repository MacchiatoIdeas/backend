from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from users.permissions import *

from .serializers import *

class AutomatedExerciseViewSet(viewsets.ModelViewSet):
    queryset = AutomatedExercise.objects.all()
    serializer_class = AutomatedExerciseSerializer

    permission_classes = (AuthenticatedTeacher,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user.teacher)
