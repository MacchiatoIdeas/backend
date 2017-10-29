from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'', views.UserViewSet)

urlpatterns = [
    url(r'^me/', views.GetMe.as_view()),
    url(r'^', include(router.urls)),
]
