from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from material.models import Subject
from exercises.models import AutomatedExercise,AutomatedExerciseAnswer

from users.permissions import *
from .serializers import *

import datetime

import numpy as np

@api_view(['GET'])
def autoexercise_recommended(request,subject):
	# # Check if user is authenticated and has
	if request.user.is_anonymous():
		answs = AutomatedExerciseAnswer.objects.none()
	else:
		answs = request.user.answers
	n_answs = answs.count()
	#
	subj = get_object_or_404(Subject,name=subject)
	conts = subj.contents.all()
	#
	contscores = []
	for cont in conts:
		#
		contansws = answs.filter(exercise__content=cont)
		for answ in contansws.all():
			deltats.append((datetime.datetime.now()-answ.moment).seconds)
			scores.append(answ.get_score() if answ.tscore is None else answ.tscore)
		deltats = np.array([2592000.0*5]+deltats)
		scores = np.array([1.0]+scores)
		# Get the coeficient of error
		errorweights = np.exp(-deltats/2592000.0/3.0)
		error = np.sum((1.0-scores)*errorweights)/np.sum(errorweights)
		# Get the mean time proximity
		proximal = np.mean(np.exp(-deltats/2592000.0))
		#
		contscores.append(proximal*(0.35+0.65*error))
	# Start choosing exercises randomly:
	print(zip(conts,contscores))

	# serializer = SnippetSerializer(snippets, many=True)
    # return Response(serializer.data)

	#exercises = AutomatedExercise.objects.filter(content__subject=subj)
	#answs = request.user.answers.count()




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
				query = query.filter(primitive__contains=w)
		return query

class AutomatedExerciseAnswerViewSet(viewsets.ModelViewSet):
	queryset = AutomatedExerciseAnswer.objects.all()
	serializer_class = AutomatedExerciseAnswerSerializer

	permission_classes = (AuthenticatedTeacherEdits,)

	def get_serializer_class(self):
		if self.action in ('create',):
			return AutomatedExerciseAnswerInputSerializer
		return super().get_serializer_class()

	def perform_create(self, serializer):
		serializer.save(user=self.request.user)


class ExerciseCommentViewSet(viewsets.ModelViewSet):
	queryset = ExerciseComment.objects.all()
	serializer_class = ExerciseCommentSerializer

	def perform_create(self, serializer):
		serializer.save(user=self.request.user)
