from django.db import models

class User(models.Model):
	firstName = models.CharField(max_length=30)
	lastName = models.CharField(max_length=30)

	def __init__(self):
		pass


class Student(User):
	course = models.ForeignKey(Course, on_delete=models.CASCADE)

	def __init__(self):
		pass


class Teacher(User):
	def __init__(self):
		pass


class Area(models.Model):
	name = models.CharField(max_length=50, unique=True)

	def __init__(self):
		pass


class Unit(models.Model):
	name = models.CharField(max_length=50, unique=True)
	area = models.ForeignKey(Area, on_delete=models.CASCADE)

	def __init__(self):
		pass


class SubUnit(models.Model):
	name = models.CharField(max_length=50, unique=True)
	unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
	matter = models.ForeignKey(SubjectMatter, on_delete=models.CASCADE)
	exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)

	def __init__(self):
		pass


class Guide(models.Model):
	name = models.CharField(max_length=50)
	course = models.ForeignKey(Course, on_delete=models.CASCADE)
	teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

	def __init__(self):
		pass


class Exercise(models.Model):
	subunit = models.ForeignKey(SubUnit, on_delete=models.CASCADE)
	guide = models.ForeignKey(Guide, on_delete=models.CASCADE)
	teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

	def __init__(self):
		pass


class SubjectMatter(models.Model):
	subunit = models.ForeignKey(SubUnit, on_delete=models.CASCADE)
	guide = models.ForeignKey(Guide, on_delete=models.CASCADE)
	teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

	def __init__(self):
		pass


class Answer(models.Model):
	guide = models.ForeignKey(Guide, on_delete=models.CASCADE)
	exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
	student = models.ForeignKey(Student, on_delete=models.CASCADE)

	def __init__(self):
		pass


class Correction(models.Model):
	answer = models.ForeignKey(Answer, on_delete=models.CASCADE)

	def __init__(self):
		pass


class Comment(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
	matter = models.ForeignKey(SubjectMatter, on_delete=models.CASCADE)

	def __init__(self):
		pass


class Course(models.Model):
	teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
	student = models.ForeignKey(Student, on_delete=models.CASCADE)

	def __init__(self):
		pass