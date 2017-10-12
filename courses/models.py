from django.db import models

from users.models import Teacher

class Course(models.Model):
    name = models.TextField(max_length=128)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    participants = models.ManyToManyField("auth.User")

class CourseLink(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE,
        related_name='clinks')
    guide = models.ForeignKey("material.Guide", on_delete=models.CASCADE)
