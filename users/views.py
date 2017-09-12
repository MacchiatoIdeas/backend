from django.contrib.auth.models import User, Group
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope
from .serializers import GenericUserSerializer, GroupSerializer


class UserViewSet(ModelViewSet):
	permission_classes = [IsAuthenticated, TokenHasReadWriteScope]
	queryset = User.objects.all()
	serializer_class = GenericUserSerializer


class GroupViewSet(ModelViewSet):
	permission_classes = [IsAuthenticated, TokenHasScope]
	required_scopes = ['groups']
	queryset = Group.objects.all()
	serializer_class = GroupSerializer
