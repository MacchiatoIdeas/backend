from django.test import TestCase

from .models import *
from django.contrib.auth.models import User
from users.models import AppuntaTeacher

# Program testing can be used to show the presence of bugs, but never to show their absence! - Edsger Dijkstra <(^_^)>

class QuestionModelTests(TestCase):
    def setUp(self):
        self.user = User()
        self.user.username = "Test Boy"
        self.user.password = "strong_password"
        self.user.email = "example@mail.com"
        self.user.save()
        self.teacher = AppuntaTeacher
        self.teacher.user = self.user
        self.teacher.save()

    def test_create_an_alternative_automatedexercise(self):
        """
        Checks if a single alternative exercise can be created, and check if check_right_answer_right passes.
        """
        ex = AutomatedExercise()
        ex.content = '''{
            "schema" : "alternatives",
            "alts" : ["Not right!","I am the right one!","Also not right!"]
        }'''
        ex.right_answer = '''{
            "schema" : "alternatives",
            "answer" : 1
        }'''
        #
        ex.author = self.teacher
        ex.full_clean()
        self.assertIs(ex.check_right_answer_right(),True)

    def test_create_an_matching_automatedexercise(self):
        """
        Checks if a single matching exercise can be created, and check if check_right_answer_right passes.
        """
        ex = AutomatedExercise()
        ex.content = '''{
            "schema" : "matching",
            "sideA" : ["Decimal 5","Decimal 7","Decimal 9"],
            "sideB" : ["Roman IX","Roman V","Roman VII","Roman IV"]
        }'''
        ex.right_answer = '''{
            "schema" : "matching",
            "matchs" : [1,2,0]
        }'''
        #
        ex.author = self.teacher
        ex.full_clean()
        self.assertIs(ex.check_right_answer_right(),True)

# enquiry = Enquiry(email="testtest.com")
# self.assertRaises(ValidationError, enquiry.full_clean)
