import unittest

from linkedin import Linkedin as JobProcessor
from models import Job, JobCounter

class test_getting_job_details_from_linkedin_job_post(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # This will be executed once for the test class
        cls.processor = JobProcessor()

    def setUp(self):
        # This will be executed before each test method
        pass

    def find_job_with_title(self):
        # Open the Linkedin job search page
        self.processor.openJobsSearchPage()

        # Search for any job in https://www.linkedin.com/jobs/search/
        jobs = self.processor.searchJobs()
        
        # Find the first job that contains non-empty job title
        job_with_title = next(job for job in jobs if job.title)
        return job_with_title

    def test_getting_job_title_from_job_post_page(self):
        job_details_from_search_page = self.find_job_with_title()
        job_title_from_search_page = job_details_from_search_page.title

        # Open page with a job with a title property
        job_details_from_job_page = self.processor.openJobDetailsPage(job_details_from_search_page.id)

        # Getting the job title
        job_title_from_job_page = job_details_from_job_page.title

        # Asserting the results
        self.assertEqual(job_title_from_job_page, job_title_from_search_page)