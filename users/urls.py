from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'^courses', views.CourseViewSet)
router.register(r'', views.UserViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
