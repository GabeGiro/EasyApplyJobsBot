from tests.base_test_class import BaseTestCase

from linkedin import Linkedin as JobProcessor
from models import JobForVerification


class test_getting_job_details_from_linkedin_job_post(BaseTestCase):

    # TODO Figure out if it's possible to achieve greater threshold percentage
    THRESHOLD = 0.2
    THRESHOLD_PERCENTAGE = int(THRESHOLD * 100)
    jobs_from_search_page = []

    @classmethod
    def setUpClass(self):
        self.processor = JobProcessor()
        self.processor.goToJobsSearchPage()
        self.jobs_from_search_page = self.processor.driverHelper.getJobsListFromSearchPage()

    
    def setUp(self):
        super().setUp()


    def tearDown(self):
        super().tearDown(self.processor.driver)


    def test_getting_job_list(self):
        # Then
        self.assertIsInstance(self.jobs_from_search_page, list)
        self.assertGreater(len(self.jobs_from_search_page), 0)


    def test_getting_job_title(self):
        # Setup
        job_titles = []

        # When
        for job in self.jobs_from_search_page:
            job_title = self.processor.getJobTitleFromJobCardInSearchResults(job)
            job_titles.append(job_title)

        # Then
        successful_assertions = 0
        for title in job_titles:
            if title is not None and isinstance(title, str) and len(title) > 0:
                successful_assertions += 1
    
        total_items = len(job_titles)
        self.assertGreaterEqual(successful_assertions, self.THRESHOLD * total_items, f'Less than {self.THRESHOLD_PERCENTAGE}% of job titles are valid')


    def test_getting_job_company(self):
        # Setup
        job_companies = []

        # When
        for job in self.jobs_from_search_page:
            job_company = self.processor.getCompanyNameFromJobCardInSearchResults(job)
            job_companies.append(job_company)

        # Then
        successful_assertions = 0
        for company in job_companies:
            if company is not None and isinstance(company, str) and len(company) > 0:
                successful_assertions += 1

        total_items = len(job_companies)
        self.assertGreaterEqual(successful_assertions, self.THRESHOLD * total_items, f'Less than {self.THRESHOLD_PERCENTAGE}% of company names are valid')
        

    def test_getting_job_workplace_type(self):
        # Setup
        possible_workplace_types = ['Remote', 'On-site', 'Hybrid']
        job_workplace_types = []

        # When
        for job in self.jobs_from_search_page:
            job_workplace_type = self.processor.getWorkplaceTypeFromJobCardInSearchResults(job)
            job_workplace_types.append(job_workplace_type)

        # Then
        successful_assertions = 0
        for workplace_type in job_workplace_types:
            if workplace_type is not None and isinstance(workplace_type, str) and workplace_type in possible_workplace_types:
                successful_assertions += 1

        total_items = len(job_workplace_types)
        self.assertGreaterEqual(successful_assertions, self.THRESHOLD * total_items, f'Less than {self.THRESHOLD_PERCENTAGE}% of workplace types are valid')
