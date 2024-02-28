import unittest

from linkedin import Linkedin as JobProcessor
import repository_wrapper as backend
from models import Job


class test_handling_questions(unittest.TestCase):

    job_id_with_unanswered_question_that_does_not_exist_on_backend = "3772904478" # TODO: Change this to a job with a question 
    unanswered_question_that_does_not_exist_on_backend = "What is your favorite color?" # TODO: Change this to a question that does not exist on the backend

    job_id_with_unanswered_question_existing_on_backend = "3772904478" # TODO: Change this to a job with a question
    unanswered_question_that_exists_on_backend = "What is your favorite color?" # TODO: Change this to a question that exists on the backend


    @classmethod
    def setUpClass(cls):
        # This will be executed once for the test class
        cls.processor = JobProcessor()
        backend.init()

        cls.assertTrue(cls.backend.initialized)


    def test_unanswered_question_does_not_exist_on_backend_exists_on_linkedin(self):
        """Test if Unanswered Question does NOT EXIST on the Backend but EXISTS on LinkedIn"""

        # Get the job from the backend
        job = backend.get_job(self.job_id_with_unanswered_question_that_does_not_exist_on_backend)

        # Assert that none of the questions is the same as the one we have
        self.assertNotIn(self.unanswered_question_that_does_not_exist_on_backend, job.questions)

        # Get the job with the bot
        self.processor.processJob(self.job_id_with_unanswered_question_that_does_not_exist_on_backend)

        # Assert that the question was passed as an argument to backend for verification
        self.backend.verify_questions.assert_called_with([job])


    def test_unanswered_question_exists_on_backend(self):
        """Test if Unanswered Question EXISTS on the Backend"""

        # Get the job from the backend
        job = backend.get_job(self.job_id_with_unanswered_question_existing_on_backend)

        # Assert that the job has a question on the backend
        self.assertTrue(job.questions)

        # Assert that one of the questions is the same as the one we have
        self.assertIn(self.unanswered_question_that_exists_on_backend, job.questions)


    def test_unanswered_question_exists_on_backend_also_exists_on_linkedin(self):
        """Test if Unanswered Question EXISTS on the Backend and ALSO EXISTS on LinkedIn"""
        
        # Get the job with the bot
        self.processor.processJob(self.job_id_with_unanswered_question_existing_on_backend)

        # Assert that the question was passed to backend for verification
        self.assertTrue(self.backend.verify_jobs.called)


# def test_question_and_answer_existing_on_backend(self):
        
# def test_question_and_answer_existing_on_backend_but_answer_differs_from_linkedin_session_answer(self):

# def test_saving_answered_question_which_does_not_exist_on_backend(self):
        


# class test_answered_question_which_exists_on_backend(unittest.TestCase):
#     pass


# class test_unanswered_question_which_does_not_exist_on_backend(unittest.TestCase):
#     pass


# class test_unanswered_question_which_exists_on_backend(unittest.TestCase):
#     pass


# class test_handling_single_line_text_input_answer(unittest.TestCase):
#     pass


# class test_handling_multi_line_text_input_answer(unittest.TestCase):
#     pass


# class test_handling_single_choice_answer(unittest.TestCase):
#     pass


# class test_handling_dropdown_answer(unittest.TestCase):
#     pass


# class test_handling_write_to_dropdown_answer(unittest.TestCase):
#     pass