from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from material.serializers import *
from users.permissions import *

from .models import *


class FieldOfStudyViewSet(viewsets.ModelViewSet):
    queryset = FieldOfStudy.objects.all()
    serializer_class = FieldOfStudySerializer

    def get_serializer_class(self):
        if self.action in ('list',):
            return FieldOfStudyListSerializer
        if self.action in ('retrieve',):
            return FieldOfStudyRetrieveSerializer
        return super().get_serializer_class()


class UnitViewSet(viewsets.ModelViewSet):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer

    def get_serializer_class(self):
        if self.action in ('list',):
            return UnitListSerializer
        return super().get_serializer_class()


class ContentViewSet(viewsets.ModelViewSet):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer

    permission_classes = (AuthenticatedTeacher,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user.teacher)

    def get_serializer_class(self):
        if self.action in ('list',):
            return ContentListSerializer
        if self.action in ('retrieve',):
            return ContentRetrieveSerializer
        return super().get_serializer_class()


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    permission_classes = (IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FeedbackCommentViewSet(viewsets.ModelViewSet):
    queryset = FeedbackComment.objects.all()
    serializer_class = FeedbackCommentSerializer

    permission_classes = (IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
