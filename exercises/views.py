from rest_framework import viewsets

from users.permissions import *
from .serializers import *


class AutomatedExerciseViewSet(viewsets.ModelViewSet):
	queryset = AutomatedExercise.objects.all()
	serializer_class = AutomatedExerciseSerializer

	permission_classes = (AuthenticatedTeacher,)

	def perform_update(self, serializer):
		instance = serializer.save(author=self.request.user.teacher)
		instance.primitive = instance.make_primitive()
		instance.save()

	def perform_create(self, serializer):
		self.perform_update(serializer)

	def get_queryset(self):
		search = self.request.GET.get('s', '')
		query = AutomatedExercise.objects.all()
		if search!='':
			words = primitivize_string(search).split(" ")
			for w in words:
				query = query.filter(primitive__icontains=w)
		return query

class AutomatedExerciseAnswerViewSet(viewsets.ModelViewSet):
	queryset = AutomatedExerciseAnswer.objects.all()
	serializer_class = AutomatedExerciseAnswerSerializer

	def perform_create(self, serializer):
		serializer.save(user=self.request.user)
