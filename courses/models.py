from django.db import models

from users.models import Teacher
from exercises.models import AutomatedExerciseAnswer

class Course(models.Model):
	name = models.TextField(max_length=128)
	teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
	participants = models.ManyToManyField("auth.User")

class CourseLink(models.Model):
	course = models.ForeignKey(Course, on_delete=models.CASCADE,
		related_name='clinks')
	guide = models.ForeignKey("material.Guide", on_delete=models.CASCADE)

	def get_answers(self):
		querry = AutomatedExerciseAnswer.objects
		querry = querry.filter(user__course=self.course)
		querry = querry.filter(exercise__guideitem__guide=self.guide)
		return querry.all()
