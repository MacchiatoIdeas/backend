from django.test import TestCase

# Program testing can be used to show the presence of bugs, but never to show their absence! - Edsger Dijkstra <(^_^)>

class QuestionModelTests(TestCase):
    def create_an_alternative_automatedexercise(self):
        """
        Checks if a single alternative exercise can be created, and check if check_right_answer_right passes.
        """
        ex = AutomatedExercise()
        ex.exercise = '''{
            "schema" : "alternatives",
            "alts" : ["Not right!","I am the right one!","Also not right!"],
        }'''
        ex.right_answer = '''{
            "schema" : "alternatives",
            "answer" : 1
        }'''
        self.assertIs(ex.check_right_answer_right(),True)
        ex.full_clean()

    def create_an_matching_automatedexercise(self):
        """
        Checks if a single matching exercise can be created, and check if check_right_answer_right passes.
        """
        ex = AutomatedExercise()
        ex.exercise = '''{
            "schema" : "matching",
            "side_a" : ["Decimal 5","Decimal 7","Decimal 9"],
            "side_b" : ["Roman IX","Roman V","Roman VII","Roman IV"],
        }'''
        ex.right_answer = '''{
            "schema" : "matching",
            "answer" : [1,2,0]
        }'''
        self.assertIs(ex.check_right_answer_right(),True)
        ex.full_clean()

# enquiry = Enquiry(email="testtest.com")
# self.assertRaises(ValidationError, enquiry.full_clean)
