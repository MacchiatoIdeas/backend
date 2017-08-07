from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'content', views.ContentViewSet)
router.register(r'field-of-study', views.FieldOfStudyViewSet)
router.register(r'unit', views.UnitViewSet)
router.register(r'sub-unit', views.SubUnitViewSet)


urlpatterns = [
    url(r'^', include(router.urls)),
]
