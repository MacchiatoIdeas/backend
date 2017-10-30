from rest_framework import viewsets
from .serializers import GallerySerializer
from .models import Gallery

from rest_framework.permissions import AllowAny

class GalleryViewSet(viewsets.ModelViewSet):
	queryset = Gallery.objects.all()
	serializer_class = GallerySerializer
	permission_classes = [AllowAny]