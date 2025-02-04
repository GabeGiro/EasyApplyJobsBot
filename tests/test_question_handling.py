from base_test_class import BaseTestCase

from linkedin import Linkedin as JobProcessor
from models import JobForVerification, JobCounter
from typing import List


class test_getting_job_details_from_linkedin_job_post(BaseTestCase):

    job_with_unanswered_questions: JobForVerification

    @classmethod
    def setUpClass(cls):
        # This will be executed once for the test class
        cls.processor = JobProcessor()

        # Get the jobs from the search page
        easy_apply_jobs_from_search_page = cls.find_easy_apply_jobs_from_search_page()


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
            cls.processor.clickEasyApplyButton()
            is_application_popup_displayed = cls.processor.isApplicationPopupDisplayed()
            cls.assertTrue(is_application_popup_displayed, "Application popup is not displayed")
            job_that_has_pages_with_questions = cls.processor.isNextButtonDisplayed()
            if not job_that_has_pages_with_questions:
                continue

            cls.assertTrue(job_that_has_pages_with_questions, "Job does not have pages with questions")
            cls.processor.clickNextButton()
            # TODO Finish this method



    def setUp(self):
        super().setUp()


    def tearDown(self):
        super().tearDown(self.processor.driver)


    # TODO test_gracefully_canceling_job_application_without_answers
    def test_gracefully_canceling_job_application_without_answers(self):
        # Go to the first job
        easy_apply_job = self.easy_apply_jobs_from_search_page[0]
        self.processor.goToJobPage(easy_apply_job.linkedinJobId)

        # Click the Easy Apply button
        self.processor.clickEasyApplyButton()

        # Check if the application popup is displayed
        is_application_popup_displayed = self.processor.isApplicationPopupDisplayed()
        self.assertTrue(is_application_popup_displayed, "Application popup is not displayed")

        # Click through the application process
        while self.processor.isApplicationStepDisplayed():
            self.processor.clickNextButton()

        # Check if the Review button is displayed
        is_last_application_step_displayed = self.processor.isLastApplicationStepDisplayed()
        self.assertTrue(is_last_application_step_displayed, "Last application step is not displayed")

        # Click the Review button
        self.processor.clickReviewApplicationButton()

        # Check if the Submit button is displayed
        is_review_application_step_displayed = self.processor.isReviewApplicationStepDisplayed()
        self.assertTrue(is_review_application_step_displayed, "Review application step is not displayed")

        # Click the Submit button
        self.processor.clickSubmitApplicationButton()

        # Check if the application was submitted
        is_application_submitted_dialog_displayed = self.processor.isApplicationSubmittedDialogDisplayed()
        self.assertTrue(is_application_submitted_dialog_displayed, "Application submitted dialog is not displayed")


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
