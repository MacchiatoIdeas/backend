from django.db import models
from oauth2_provider.models import AbstractAccessToken


class Teacher(models.Model):
    user = models.OneToOneField("auth.User",
                                on_delete=models.CASCADE,
                                related_name='teacher')

    def __str__(self):
        return self.user.get_full_name()


class AppuntaAdmin(models.Model):
    user = models.OneToOneField("auth.User",
                                on_delete=models.CASCADE,
                                related_name='appunta_admin')

class Course(models.Model):
    name = models.TextField(max_length=128)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    participants = models.ManyToManyField("auth.User")

class CourseLink(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE,
        related_name='clinks')
    guide = models.ForeignKey("material.Guide", on_delete=models.CASCADE)
