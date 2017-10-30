from django.db import models

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone

import json
import jsonschema

from primitivizer import primitivize_string

from material.models import parse_json,validate_entries

MAX_ANSWER_LENGTH = 255

exercise_schema = {
	"type": "object",
	"oneOf": [
		{
			"properties": {
				"schema": {"type": "string", "pattern": "alternatives"},
				"alts": {
					"type": "array",
					"items": {"type": "string"},
					"minItems": 1,
				},
			},
			"required": ["schema", "alts"],
			"additionalProperties": False,
		}, {
			"properties": {
				"schema": {"type": "string", "pattern": "matching"},
				"sideA": {
					"type": "array",
					"items": {"type": "string"},
					"minItems": 1,
				},
				"sideB": {
					"type": "array",
					"items": {"type": "string"},
					"minItems": 1,
				},
			},
			"required": ["schema", "sideA", "sideB"],
			"additionalProperties": False,
		}, {
			"properties": {
				"schema": {"type": "string", "pattern": "completion"},
				"text": {"type": "string", "pattern": ".*\?\?.*"},
			},
			"required": ["schema", "text"],
			"additionalProperties": False,
		}, {
			"properties": {
				"schema": {"type": "string", "pattern": "trueorfalse"},
				"sentences": {
					"type": "array",
					"items": {"type": "string"},
					"minItems": 1,
				},
			},
			"required": ["schema", "sentences"],
			"additionalProperties": False,
		},
	],
}

answer_schema = {
	"type": "object",
	"oneOf": [
		{
			"properties": {
				"schema": {"type": "string", "pattern": "alternatives"},
				"answer": {"type": "integer"},
			},
			"required": ["schema", "answer"],
			"additionalProperties": False,
		}, {
			"properties": {
				"schema": {"type": "string", "pattern": "matching"},
				"matchs": {
					"type": "array",
					"items": {"type": "integer"},
				},
			},
			"required": ["schema", "matchs"],
			"additionalProperties": False,
		}, {
			"properties": {
				"schema": {"type": "string", "pattern": "completion"},
				"words": {
					"type": "array",
					"items": {"type": "string"},
				},
			},
			"required": ["schema", "words"],
			"additionalProperties": False,
		}, {
			"properties": {
				"schema": {"type": "string", "pattern": "trueorfalse"},
				"choices": {
					"type": "array",
					"items": {"type": "boolean"},
					"minItems": 1,
				},
			},
			"required": ["schema", "choices"],
			"additionalProperties": False,
		},
	],
}


################################################################
# VALIDATORS:
################################################################

def validate_exercise(content):
	parsed = parse_json(content, exercise_schema)


def validate_answer(content):
	parsed = parse_json(content, answer_schema)


# NOTE: schema specific validations should go here.


def check_right_answer_right(content, right_answer):
	"""
	Checks if the right answer is appropiate for the exercise.
	"""
	exerc = json.loads(content)
	ransw = json.loads(right_answer)
	# Check if it is the same schema:
	if ransw["schema"] != exerc["schema"]: return False
	# Evaluate each different schema:
	if ransw["schema"] == "alternatives":
		if ransw["answer"] < 0 or ransw["answer"] >= len(exerc["alts"]):
			return False
	elif ransw["schema"] == "matching":
		# Check if there are repeated matchs:
		if len(ransw["matchs"]) != len(set(ransw["matchs"])):
			return False
		# Check if one match is invalid:
		are_bad = [x < 0 or x >= len(exerc['sideB'])
		           for x in ransw["matchs"]]
		if any(are_bad):
			return False
		# Check if there are an incorrect number of matchs:
		if len(ransw["matchs"]) != len(exerc["sideA"]):
			return False
	elif ransw["schema"] == "completion":
		slots = len(exerc["text"].split("??")) - 1
		if slots != len(ransw["words"]):
			return False
	elif ransw["schema"] == "trueorfalse":
		if len(exerc["sentences"]) != len(ransw["choices"]):
			return False
	return True


class AutomatedExercise(models.Model):
	"""
	An exercise that can come in many formats and can be automatically evaluated.
	"""
	difficulty = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(4)])
	# | Author owner of this exercise:
	author = models.ForeignKey("users.AppuntaTeacher", related_name='exercises', on_delete=models.CASCADE)
	# | Unit of the exercise:
	unit = models.ForeignKey("material.Unit", related_name='exercises', on_delete=models.CASCADE)

	moment = models.DateTimeField(auto_now_add=True)

	# | Briefing of the exercise:
	briefing = models.TextField(blank=True, default="")

	# | Text of the exercise:
	text = models.TextField(validators=[validate_entries])

	# | Content of the exercise:
	content = models.TextField(validators=[validate_exercise])
	# | Exercise's right answer:
	right_answer = models.CharField(validators=[validate_answer],
	                                max_length=MAX_ANSWER_LENGTH)

	def __str__(self):
		return "id: {0}, schema: {1}".format(self.id, self.schema())

	def schema(self):
		exerc = json.loads(self.content)
		return exerc["schema"]

	# Primitivized version for searching
	primitive = models.TextField(blank=True)

	def make_primitive(self):
		return primitivize_string(" ".join([
			str(self.author), self.briefing]))


class AutomatedExerciseAnswer(models.Model):
	# | The user that answered:
	user = models.ForeignKey('auth.User', on_delete=models.CASCADE,related_name='answers')
	# | The answered exercise:
	exercise = models.ForeignKey(AutomatedExercise, on_delete=models.CASCADE)
	# | The given answer:
	answer = models.CharField(validators=[validate_answer],
	                          max_length=MAX_ANSWER_LENGTH)
	# | Score gave by a teacher:
	tscore = models.FloatField(blank=True,null=True)
	# | When the exercise was answered
	moment = models.DateTimeField(auto_now_add=True)

	def get_score(self):
		# TODO: Think if two matchs pointing to the same index give score.
		answ = json.loads(self.answer)
		ransw = json.loads(self.exercise.right_answer)
		# Check if it is the same schema:
		if answ["schema"] != ransw["schema"]: return 0
		# Evaluate each different schema:
		if ransw["schema"] == "alternatives":
			return float(answ["answer"] == ransw["answer"])
		elif ransw["schema"] == "matching":
			ml = min(len(answ["matchs"]), len(ransw["matchs"]))
			score = 0.0
			for i in range(ml):
				score += float(ransw["matchs"][i] == answ["matchs"][i])
			return score / len(ransw["matchs"])
		elif ransw["schema"] == "completion":
			ml = min(len(answ["words"]), len(ransw["words"]))
			score = 0.0
			for i in range(ml):
				score += float(ransw["words"][i].upper() == answ["words"][i].upper())
			return score / len(ransw["words"])
		elif ransw["schema"] == "trueorfalse":
			ml = min(len(answ["choices"]), len(ransw["choices"]))
			score = 0.0
			for i in range(ml):
				score += float(ransw["choices"][i] == answ["choices"][i])
			return score / len(ransw["choices"])

	# TODO: Delete all existings entries once a teacher creates a new
	# related CourseLink, check what happens when there are two,
	# Use time semantics OR add nullable courselink FK.

	# class Meta:
	# 	unique_together = ('user','exercise')


class ExerciseComment(models.Model):
	"""
    Comment on a exercise.
    """

	# user who wrote the comment
	user = models.ForeignKey('auth.User',
	                         related_name='exercise_comments',
	                         on_delete=models.CASCADE)

	# exercise related
	exercise = models.ForeignKey(AutomatedExercise,
	                             related_name='comments',
	                             on_delete=models.CASCADE)

	# text of this comment
	text = models.TextField()

	date = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.text
