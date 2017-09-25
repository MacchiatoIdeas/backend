from django.conf.urls import url,include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'exercises', views.AutomatedExerciseViewSet)
router.register(r'answers', views.AutomatedExerciseAnswerViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
