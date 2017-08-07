from __future__ import unicode_literals

from django.db import models

"""
###########################################################
USERS:
###########################################################
"""

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    forename = models.CharField(max_length=30)
    fst_surname = models.CharField(max_length=30)
    snd_surname = models.CharField(max_length=30)

    def __init__(self):
        pass

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    forename = models.CharField(max_length=30)
    fst_surname = models.CharField(max_length=30)
    snd_surname = models.CharField(max_length=30)

    def __init__(self):
        pass

class Course(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    students = models.ManyToManyField(Student)

    def __init__(self):
        pass

"""
###########################################################
CONTENT:
###########################################################
"""

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

    def __init__(self):
        pass

class Exercise(models.Model):
    subunits = models.ManyToManyField(SubUnit)
    author = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    def __init__(self):
        pass

class SubjectMatter(models.Model):
    subunits = models.ManyToManyField(Student)
    author = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    def __init__(self):
        pass

"""
###########################################################
GUIDES:
###########################################################

ExerciseOnGuide and SubjectMatterOnGuide are extensions (of Exercise and SubjectMatter respectively) that are to appear on guides, their inherited values are intended to hold a copy of the values of what they are extending at the time they were created. This is done in order to avoid problems that may happen if a guide is distributed (or even answered) and after that its contents are modified.

NOTE: The inherited *autor* field must be ignored on ExerciseOnGuide and SubjectMatterOnGuide, since the "owner teacher" is accessed through the guide. This is an important consideration for security permissions.

Answers that point to an ExerciseOnGuide are answers to a particular guide, while Answers that point to an Exercise are system-wide answers.
"""

class ExerciseOnGuide(Exercise):
    original_exercise = models.ForeignKey(Exercise,
                                          on_delete=models.SET_NULL, null=True)
    guide = models.ForeignKey(Guide, on_delete=models.CASCADE)
    ordering = models.IntegerField()

    def __init__(self):
        pass

class SubjectMatterOnGuide(SubjectMatter):
    original_smatter = models.ForeignKey(SubjectMatter,
                                         on_delete=models.SET_NULL, null=True)
    guide = models.ForeignKey(Guide, on_delete=models.CASCADE)
    ordering = models.IntegerField()

    def __init__(self):
        pass

class Guide(models.Model):
    name = models.CharField(max_length=100)
    exercises = models.ManyToManyField(ExerciseOnGuide)
    smatters = models.ManyToManyField(SubjectMatterOnGuide)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    def __init__(self):
        pass

class Answer(models.Model):
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
    exercise = models.ForeignKey(Exercise,
                                 on_delete=models.CASCADE, null=True)
    smatter = models.ForeignKey(SubjectMatter,
                                on_delete=models.CASCADE, null=True)

    def __init__(self):
        pass
