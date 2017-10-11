from rest_framework import viewsets

from material.serializers import *
from users.permissions import *
from .models import *

from primitivizer import primitivize_string

class SubjectViewSet(viewsets.ModelViewSet):
	queryset = Subject.objects.all()
	serializer_class = SubjectSerializer

	permission_classes = (AuthenticatedAppuntaAdmin,)

	def get_serializer_class(self):
		if self.action in ('list',):
			return SubjectListSerializer
		if self.action in ('retrieve',):
			return SubjectRetrieveSerializer
		return super().get_serializer_class()


class UnitViewSet(viewsets.ModelViewSet):
	queryset = Unit.objects.all()
	serializer_class = UnitSerializer

	permission_classes = (AuthenticatedAppuntaAdmin,)

	def get_serializer_class(self):
		if self.action in ('list',):
			return UnitListSerializer
		elif self.action in ('retrieve',):
			return UnitRetrieveSerializer
		return super().get_serializer_class()


class ContentViewSet(viewsets.ModelViewSet):
	queryset = Content.objects.all()
	serializer_class = ContentSerializer

	permission_classes = (AuthenticatedTeacher,)

	def perform_update(self, serializer):
		instance = serializer.save(author=self.request.user.teacher)
		instance.primitive = instance.make_primitive()
		instance.save()

	def perform_create(self, serializer):
		self.perform_update(serializer)

	def get_serializer_class(self):
		if self.action in ('list',):
			return ContentListSerializer
		if self.action in ('retrieve',):
			return ContentRetrieveSerializer
		return super().get_serializer_class()

	def get_queryset(self):
		search = self.request.GET.get('s', '')
		query = AutomatedExercise.objects.all()
		if search!='':
			words = primitivize_string(search).split(" ")
			for w in words:
				query = query.filter(primitive__contains=w)
		return query


class CommentViewSet(viewsets.ModelViewSet):
	queryset = Comment.objects.all()
	serializer_class = CommentSerializer

	def perform_create(self, serializer):
		serializer.save(user=self.request.user)


class FeedbackCommentViewSet(viewsets.ModelViewSet):
	queryset = FeedbackComment.objects.all()
	serializer_class = FeedbackCommentSerializer

	def perform_create(self, serializer):
		serializer.save(user=self.request.user)


class GuideViewSet(viewsets.ModelViewSet):
	queryset = Guide.objects.all()
	serializer_class = GuideSerializer

	def perform_create(self, serializer):
		serializer.save(user=self.request.user)

	def get_serializer_class(self):
		if self.action in ('list',):
			return GuideListSerializer
		return super().get_serializer_class()
