from rest_framework import viewsets

from material.serializers import *
from material.permissions import *


class FieldOfStudyViewSet(viewsets.ModelViewSet):
    queryset = FieldOfStudy.objects.all()
    serializer_class = FieldOfStudySerializer


class UnitViewSet(viewsets.ModelViewSet):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer


class SubUnitViewSet(viewsets.ModelViewSet):
    queryset = SubUnit.objects.all()
    serializer_class = SubUnitSerializer


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
