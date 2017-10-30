from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'', views.UserViewSet)

urlpatterns = [
    url(r'^teachers/register', views.AppuntaTeacherRegisterView.as_view()),
    url(r'^students/register', views.AppuntaStudentRegisterView.as_view()),
    url(r'^me/', views.GetMe.as_view()),
    url(r'^', include(router.urls)),
]
