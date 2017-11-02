import random

from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from material.models import Subject,Unit
from exercises.models import AutomatedExercise,AutomatedExerciseAnswer

from users.permissions import *
from .serializers import *


import datetime

import numpy as np

@api_view(['GET'])
def autoexercise_recommended(request,subject):
	# # Check if user is authenticated and has
	if request.user.is_anonymous() or not hasattr(self.request.user,'student'):
		answs = AutomatedExerciseAnswer.objects.none()
	else:
		answs = request.user.student.answers
	n_answs = answs.count()
	#
	subj = get_object_or_404(Subject,name=subject)
	units = Unit.objects.filter(subject=subj)
	#
	unitscores = []
	for uni in units:
		#
		deltats = []
		scores = []
		unitansws = answs.filter(exercise__unit=uni)
		for answ in unitansws.all():
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
		unitscores.append(proximal*(0.35+0.65*error))
	# Start choosing exercises randomly:
	returned = []
	exercises = [c.exercises for c in units]
	number = int(request.GET.get("n","20"))
	while len(exercises)>0 and len(returned)<number:
		ko = np.sum(unitscores)*np.random.random()
		for indx in range(len(exercises)):
			ko -= unitscores[indx]
			if ko<=0: break
		if exercises[indx].count() == 0:
			del exercises[indx]
			del unitscores[indx]
			continue
		random_pk = random.choice([exe.pk for exe in exercises[indx].all()])
		exercise = exercises[indx].get(pk=random_pk)
		exercises[indx] = exercises[indx].exclude(pk=random_pk)
		returned.append(exercise)
	serializer = AutomatedExerciseListSerializer(returned,many=True)
	return Response(serializer.data)

@api_view(['GET'])
def answers_to_exercise(request,exercise_id):
	if request.user.is_anonymous() or not hasattr(request.user,'student'):
		answs = AutomatedExerciseAnswer.objects.none()
	else:
		answs = request.user.student.answers.filter(exercise=exercise_id)
	serializer = AutomatedExerciseAnswerSerializer(answs,many=True)
	return Response(serializer.data)


class AutomatedExerciseViewSet(viewsets.ModelViewSet):
	queryset = AutomatedExercise.objects.all()
	serializer_class = AutomatedExerciseSerializer

	permission_classes = [AuthenticatedTeacher,IsAuthor]

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

	def get_serializer_class(self):
		if self.action in ('retrieve',):
			return AutomatedExerciseRetrieveSerializer
		return super().get_serializer_class()


class AutomatedExerciseAnswerViewSet(viewsets.ModelViewSet):
	queryset = AutomatedExerciseAnswer.objects.all()
	serializer_class = AutomatedExerciseAnswerSerializer

	permission_classes = (AutomatedExerciseAnswerPermission,)

	def get_serializer_class(self):
		if self.action in ('create',):
			return AutomatedExerciseAnswerInputSerializer
		return super().get_serializer_class()

	def perform_create(self, serializer):
		# TODO: Only allow an AppuntaStudent to create AutomatedExerciseAnswers
		serializer.save(user=self.request.user.student)


class ExerciseCommentViewSet(viewsets.ModelViewSet):
	queryset = ExerciseComment.objects.all()
	serializer_class = ExerciseCommentSerializer

	permission_classes = (AuthenticatedAppuntaUser,)

	def perform_create(self, serializer):
		serializer.save(user=self.request.user)
