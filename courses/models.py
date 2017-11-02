from django.db import models

from users.models import AppuntaTeacher
from exercises.models import AutomatedExerciseAnswer

class Course(models.Model):
	name = models.TextField(max_length=128)
	teacher = models.ForeignKey(AppuntaTeacher, on_delete=models.CASCADE)
	participants = models.ManyToManyField("users.AppuntaStudent",related_name='courses')

	def __str__(self):
		return self.name


class CourseLink(models.Model):
	course = models.ForeignKey(Course, on_delete=models.CASCADE,
		related_name='clinks')
	guide = models.ForeignKey("material.Guide", on_delete=models.CASCADE)

	def get_answers(self):
		return AutomatedExerciseAnswer.objects\
			.filter(student__courses=self.course)\
			.filter(exercise__guideitem__guide=self.guide)
