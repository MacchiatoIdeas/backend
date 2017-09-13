from rest_framework import viewsets
from oauth2_provider.contrib.rest_framework.permissions import TokenHasResourceScope
from users.permissions import *
from .serializers import *


class AutomatedExerciseViewSet(viewsets.ModelViewSet):
    queryset = AutomatedExercise.objects.all()
    serializer_class = AutomatedExerciseSerializer

    permission_classes = (TokenHasResourceScope,)  # (AuthenticatedTeacher,)
    required_scopes = ['automatedex']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user.teacher)
