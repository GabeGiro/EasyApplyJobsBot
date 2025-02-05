from tests.base_test_class import BaseTestCase

from linkedin import Linkedin as JobProcessor
from models import JobForVerification


class test_getting_job_details_from_linkedin_job_post(BaseTestCase):

    jobs_from_search_page = []
    
    @classmethod
    def setUpClass(cls):
        # This will be executed once for the test class
        cls.processor = JobProcessor()

        # Get the jobs from the search page
        cls.jobs_from_search_page = cls.find_jobs_from_search_page()

    
    def setUp(self):
        super().setUp()


    def tearDown(self):
        super().tearDown(self.processor.driver)
