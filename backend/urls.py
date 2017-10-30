from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.routers import DefaultRouter

from django.conf.urls.static import static
from django.conf import settings

#TODO: delete not useful router?
router = DefaultRouter()

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^material/', include('material.urls', namespace='material')),
    url(r'^exercises/', include('exercises.urls', namespace='exercises')),
    url(r'^courses/', include('courses.urls', namespace='courses')),
    url(r'^users/', include('users.urls', namespace='users')),
    url(r'^gallery/', include('gallery.urls', namespace='gallery')),
    url(r'^', include(router.urls)),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Add authentication for the Browsable API
urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls',
        namespace='rest_framework')),
]