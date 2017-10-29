from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'', views.UserViewSet)
#router.register(r'teachers/register', views.AppuntaTeacherRegisterView)

urlpatterns = [
    url(r'^teachers/register', views.AppuntaTeacherRegisterView.as_view()),
    url(r'^me/', views.GetMe.as_view()),
    url(r'^', include(router.urls)),
]
