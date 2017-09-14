from django.conf.urls import url,include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'contents', views.ContentViewSet)
router.register(r'subjects', views.SubjectViewSet)
router.register(r'units', views.UnitViewSet)
router.register(r'comments', views.CommentViewSet)
router.register(r'feedback-comments', views.FeedbackCommentViewSet)
router.register(r'guides', views.GuideViewSet)


urlpatterns = [
    url(r'^', include(router.urls)),
]
