from rest_framework import viewsets
from .serializers import GallerySerializer
from .models import Gallery
from users.permissions import AuthenticatedAppuntaUser

class GalleryViewSet(viewsets.ModelViewSet):
	queryset = Gallery.objects.all()
	serializer_class = GallerySerializer
	permission_classes = [AuthenticatedAppuntaUser]

	def get_queryset(self):
		return Gallery.objects.filter(user_id__exact=self.request.user.id)

	def perform_create(self, serializer):
		serializer.save(user=self.request.user)