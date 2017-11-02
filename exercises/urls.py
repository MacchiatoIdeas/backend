from django.conf.urls import url,include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'exercises', views.AutomatedExerciseViewSet)
router.register(r'answers', views.AutomatedExerciseAnswerViewSet)
router.register(r'comments', views.ExerciseCommentViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^recommended/(?P<subject>\w+)$', views.autoexercise_recommended),
    url(r'^myanswers/(?P<exercise_id>[0-9]+)$', views.answers_to_exercise),
]
