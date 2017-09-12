from django.db import models

from django.core.exceptions import ValidationError

import json
import jsonschema

MAX_ANSWER_LENGTH = 255

exercise_schema = {
    "type" : "object",
    "oneOf" : [
        {
            "properties": {
                "schema" : {"type" : "string", "const" : "alternatives"},
                "alts" : {
                    "type" : "array",
                    "items" : {"type" : "string"},
                    "minItems" : 1,
                },
            },
            "required": ["schema","alts"],
            "additionalProperties": False,
        }, {
            "properties": {
                "schema" : {"type" : "string", "const" : "matching"},
                "sideA" : {
                    "type" : "array",
                    "items" : {"type" : "string"},
                    "minItems" : 1,
                },
                "sideB" : {
                    "type" : "array",
                    "items" : {"type" : "string"},
                    "minItems" : 1,
                },
            },
            "required": ["schema","sideA","sideB"],
            "additionalProperties": False,
        },
    ],
}

answer_schema = {
    "type" : "object",
    "oneOf" : [
        {
            "properties": {
                "schema" : {"type" : "string", "const" : "alternatives"},
                "answer" : {"type" : "integer"},
            },
            "required": ["schema","answer"],
            "additionalProperties": False,
        }, {
            "properties": {
                "schema" : {"type" : "string", "const" : "matching"},
                "matchs" : {
                    "type" : "array",
                    "items" : {"type" : "integer"},
                },
            },
            "required": ["schema","matchs"],
            "additionalProperties": False,
        },
    ],
}


################################################################
# VALIDATORS:
################################################################

def parse_json(content,schema):
    # Try to parse JSON:
    try:
        parsed = json.loads(content)
    except Exception as ex:
        raise ValidationError("Invalid JSON!")
    # Validate the JSON according to the schema:
    try:
        jsonschema.validate(parsed,schema)
    except jsonschema.exceptions.ValidationError as ex:
        raise ValidationError.create_from(str(ex))
    return parsed

def validate_exercise(content):
    parsed = parse_json(content,exercise_schema)
    # NOTE: schema specific validations should go here.

def validate_answer(content):
    parsed = parse_json(content,answer_schema)
    # NOTE: schema specific validations should go here.


class AutomatedExercise(models.Model):
    """
    An exercise that can come in many formats and can be automatically evaluated.
    """
    # | Author owner of this exercise:
    author = models.ForeignKey("users.Teacher", on_delete=models.CASCADE)
    # | Briefing of the exercise:
    briefing = models.TextField(blank=True,default="")
    # | Content of the exercise:
    content = models.TextField(validators=[validate_exercise])
    # | Exercise's right answer:
    right_answer = models.CharField(validators=[validate_answer],
        max_length=MAX_ANSWER_LENGTH)

    def check_right_answer_right(self):
        """
        Checks if the right answer is appropiate for the exercise.
        """
        exerc = json.loads(self.content)
        ransw = json.loads(self.right_answer)
        # Check if it is the same schema:
        if ransw["schema"]!=exerc["schema"]: return False
        # Evaluate each different schema:
        if ransw["schema"]=="alternatives":
            if ransw["answer"]<0 or ransw["answer"]>=len(exerc["alts"]):
                return False
        elif ransw["schema"]=="matching":
            # Check if there are repeated matchs:
            if len(ransw["matchs"])!=len(set(ransw["matchs"])):
                return False
            # Check if one match is invalid:
            are_bad = [x<0 or x>=len(exerc['sideB'])
                for x in ransw["matchs"]]
            if any(are_bad):
                return False
            # Check if there are an incorrect number of matchs:
            if len(ransw["matchs"])!=len(exerc["sideA"]):
                return False
        return True

    def calculate_score(self,answer):
        # TODO: Evaluate if two matchs pointing to the same index give score.
        answ = json.loads(answer)
        ransw = json.loads(self.right_answer)
        # Check if it is the same schema:
        if answ["schema"]!=ransw["schema"]: return 0
        # Evaluate each different schema:
        if ransw["schema"]=="alternatives":
            return float(answ["answer"]==ransw["answer"])
        elif ransw["schema"]=="matching":
            ml = min(len(answ["matchs"]),len(ransw["matchs"]))
            score = 0.0
            for i in range(ml):
                score += float(ransw["matchs"][i]==answ["matchs"][i])
            return score/len(ransw["matchs"])


class AutomatedExerciseAnswer(models.Model):
    # | The user that answered:
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    # | The answered exercise:
    exercise = models.ForeignKey(AutomatedExercise, on_delete=models.CASCADE)
    #  | The given answer:
    answer = models.CharField(validators=[validate_answer],
        max_length=MAX_ANSWER_LENGTH)
