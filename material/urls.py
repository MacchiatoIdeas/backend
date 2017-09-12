from django.conf.urls import url,include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'content', views.ContentViewSet)
router.register(r'field-of-study', views.SubjectViewSet)
router.register(r'unit', views.UnitViewSet)
router.register(r'comment', views.CommentViewSet)
router.register(r'feedback-comment', views.FeedbackCommentViewSet)


urlpatterns = [
    url(r'^', include(router.urls)),
]
