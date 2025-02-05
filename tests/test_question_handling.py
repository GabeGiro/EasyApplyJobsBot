from base_test_class import BaseTestCase

from linkedin import Linkedin as JobProcessor
from models import JobForVerification, JobCounter
from typing import List


class test_getting_job_details_from_linkedin_job_post(BaseTestCase):

    job_with_unanswered_questions: JobForVerification = None

    @classmethod
    def setUpClass(cls):
        # This will be executed once for the test class
        cls.processor = JobProcessor()

        # Get the jobs from the search page
        easy_apply_jobs_from_search_page = cls.find_easy_apply_jobs_from_search_page()
        cls.job_with_unanswered_questions = cls.find_job_with_unanswered_questions(easy_apply_jobs_from_search_page)


    # TODO extract and use this method in linkedin.py
    @classmethod
    def find_easy_apply_jobs_from_search_page(cls) -> list[JobForVerification]:
        # Open the Linkedin general job search page
        cls.processor.goToEasyApplyJobsSearchPage()

        # Get the jobs from the search page
        jobs = cls.processor.getJobsFromSearchPage()
        return jobs


    @classmethod
    def find_job_with_unanswered_questions(cls, jobs: list[JobForVerification]) -> JobForVerification:
        for job in jobs:
            cls.processor.goToJobPage(job.linkedinJobId)

            is_easy_apply_button_displayed = cls.processor.isEasyApplyButtonDisplayed()
            if not is_easy_apply_button_displayed:
                continue

            cls.processor.clickEasyApplyButton()

            is_application_popup_displayed = cls.processor.isApplicationPopupDisplayed()
            if not is_application_popup_displayed:
                continue

            while cls.processor.isNextButtonDisplayed():
                cls.processor.clickNextButton()
                if cls.processor.isQuestionsUnansweredErrorMessageDisplayed():
                    return job
                
            if cls.processor.isLastApplicationStepDisplayed():
                cls.processor.clickReviewApplicationButton()

            if cls.processor.isQuestionsUnansweredErrorMessageDisplayed():
                    return job


    def setUp(self):
        super().setUp()


    def tearDown(self):
        super().tearDown(self.processor.driver)


    # TODO test_gracefully_canceling_job_application_without_answers
    def test_gracefully_canceling_job_application_without_answers(self):
        # Setup
        job_counter = JobCounter()
        easy_apply_job = self.job_with_unanswered_questions

        # When
        self.processor.processJob(easy_apply_job.linkedinJobId, job_counter)

        # Then
        self.assertEqual(job_counter.total, 1)
        self.assertEqual(job_counter.skipped_unanswered_questions, 1)
        self.assertEqual(job_counter.applied, 0)


# TODO Add tests:
# - test_answered_question_which_does_not_exist_on_backend
# - test_answered_question_which_exist_on_backend
# - test_unanswered_question_which_does_not_exist_on_backend
# - test_unanswered_question_which_exists_on_backend
# - test_handling_single_line_text_input_answer
# - test_handling_multi_line_text_input_answer
# - test_handling_single_choice_answer
# - test_handling_dropdown_answer
# - test_handling_write_to_dropdown_answer
# - test_handling_checkbox_answer
# - test_handling_file_upload_answer
# - test_handling_date_picker_answer
# - test_handling_time_picker_answer
# - test_handling_datetime_picker_answer
