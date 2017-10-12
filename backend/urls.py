from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.routers import DefaultRouter

from users import views as uviews
from exercises import views as eviews

# Set routes

#TODO: delete not useful router?
router = DefaultRouter()

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^material/', include('material.urls', namespace='material')),
    url(r'^exercises/', include('exercises.urls', namespace='exercises')),
    url(r'^courses/', include('courses.urls', namespace='courses')),
    url(r'^users/', include('users.urls', namespace='users')),
    url(r'^', include(router.urls)),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]

# Add authentication for the Browsable API
urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls',
        namespace='rest_framework')),
]
