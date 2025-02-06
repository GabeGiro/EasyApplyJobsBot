from typing import List, Optional
import re

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


import config
import constants
import models
import repository_wrapper
import utils.file as resultFileWriter
import utils.linkedinUrlHelper as urlHelper
from utils.linkedinWebDriverHelper import WebDriverHelper
import utils.logger as logger
from utils.logger import MessageTypes
import utils.sleeper as sleeper
import utils.utils as utils


# This class is responsible for handling the LinkedIn job application process
# It uses the Selenium WebDriver to interact with the LinkedIn website
# It also uses the repository_wrapper to interact with the backend
#
# The class is responsible for:
# - Logging in to LinkedIn (done in the constructor)
# - Searching for jobs
# - Applying to jobs
# - Handling job posts
# - Handling questions
# - Handling multiple pages of the application process
# - Handling the resume selection
# - Handling the submission of the application
# - Handling the follow company checkbox
# - Handling the application of the job
class Linkedin:
    def __init__(self):
        logger.logDebugMessage("🌐 The Bot is starting", MessageTypes.INFO)

        if config.chromeDriverPath != "":
            # Specify the path to Chromedriver provided by the Alpine package
            service = ChromeService(executable_path = config.chromeDriverPath)
        else:
            service = ChromeService(ChromeDriverManager().install())
        
        self.driver = webdriver.Chrome(service = service, options = utils.chromeBrowserOptions())        
        self.driverHelper = WebDriverHelper(self.driver)
        self.wait = WebDriverWait(self.driver, 15)

        # Navigate to the LinkedIn home page to check if we're already logged in
        self.goToUrl("https://www.linkedin.com")

        if not self.driverHelper.checkIfLoggedIn():
            self.goToUrl("https://www.linkedin.com/login?trk=guest_homepage-basic_nav-header-signin")

            logger.logDebugMessage("🔄 Trying to login to linkedin...", MessageTypes.INFO)
            try:    
                sleeper.interact(lambda : self.driver.find_element(By.ID, constants.usernameID).send_keys(config.email))
                sleeper.interact(lambda : self.driver.find_element(By.ID, constants.passwordID).send_keys(config.password))
                sleeper.interact(lambda : self.driver.find_element(By.XPATH, constants.buttonSubmitLoginXPATH).click())
                self.driverHelper.checkIfLoggedIn()
            except Exception as e:
                logger.logDebugMessage("❌ Couldn't login to Linkedin by using Chrome. Please check your Linkedin credentials on config files line 7 and 8. If error continue you can define Chrome profile or run the bot on Firefox", MessageTypes.ERROR, e)
        
        repository_wrapper.init()


    def startApplying(self):
        try:
            jobCounter = models.JobCounter()

            urlData = urlHelper.generateSearchUrls()

            for url in urlData:        
                self.goToUrl(url)

                urlWords = urlHelper.urlToKeywords(url)
                
                try:
                    totalJobs = self.wait.until(EC.presence_of_element_located((By.XPATH, '//small'))).text # TODO - fix finding total jobs
                    # totalJobs = self.driver.find_element(By.XPATH,'//small').text 

                    totalSearchResultPages = utils.jobsToPages(totalJobs)

                    lineToWrite = "\n Search keyword: " + urlWords[0] + ", Location: " + urlWords[1] + ", Found " + str(totalJobs)
                    resultFileWriter.displayWriteResults(lineToWrite)

                    for searchResultPage in range(totalSearchResultPages):
                        currentSearchResultPageJobs = constants.jobsPerPage * searchResultPage
                        url = url + "&start=" + str(currentSearchResultPageJobs)
                        self.goToUrl(url)

                        jobsForVerification = self.getJobsForVerificationFromSearchPage()
                        verifiedJobs = repository_wrapper.verify_jobs(jobsForVerification)

                        for job in verifiedJobs:
                            jobCounter = self.processJob(jobID=job.linkedinJobId, jobCounter=jobCounter)
                                    
                except TimeoutException:
                    logger.logDebugMessage("0 jobs found for: " + urlWords[0] + " in " + urlWords[1], MessageTypes.ERROR)

                logger.logDebugMessage("Category: " + urlWords[0] + " in " + urlWords[1]+ " applied: " + str(jobCounter.applied) +
                    " jobs out of " + str(jobCounter.total) + ".", MessageTypes.SUCCESS)

        except Exception as e:
            logger.logDebugMessage("Unhandled exception in StartApplying", logger.MessageTypes.ERROR, e, True)

            resultFileWriter.capture_screenshot("unhandeled_exception.png")

            resultFileWriter.capture_html(self.driver, "page_source_as_unhandled_exception.html")
            


    def goToJobsSearchPage(self):
        searchUrl = urlHelper.getGeneralSearchUrl()
        self.goToUrl(searchUrl)


    def goToEasyApplyJobsSearchPage(self):
        searchUrl = urlHelper.getEasyApplySearchUrl()
        self.goToUrl(searchUrl)

    
    def goToUrl(self, url: str):
        sleeper.interact(lambda : self.driver.get(url))
        

    def goToJobPage(self, jobID: str):
        jobPage = 'https://www.linkedin.com/jobs/view/' + jobID
        self.goToUrl(jobPage)
        return jobPage


    def processJob(self, jobID: str, jobCounter: models.JobCounter):
        jobPage = self.goToJobPage(jobID)
        jobCounter.total += 1
        sleeper.sleepInBetweenBatches(jobCounter.total)

        jobProperties = self.getJobPropertiesFromJobPage(jobID)
        repository_wrapper.update_job(jobProperties)
        if self.isJobBlacklisted(company=jobProperties.company, title=jobProperties.title): 
            jobCounter.skipped_blacklisted += 1
            lineToWrite = self.getLogTextForJobProperties(jobProperties, jobCounter) + " | " + "* 🤬 Blacklisted Job, skipped!: " + str(jobPage)
            resultFileWriter.displayWriteResults(lineToWrite)
            return jobCounter

        jobCounter = self.handleJobPost(
            jobPage=jobPage, 
            jobProperties=jobProperties, 
            jobCounter=jobCounter)

        return jobCounter
    
    
    def getJobsForVerificationFromSearchPage(self) -> List[models.JobForVerification]:
        jobsListItems = self.driverHelper.getJobsListFromSearchPage()
        jobsForVerification = []

        for jobItem in jobsListItems:
            if self.driverHelper.exists(jobItem, By.XPATH, constants.appliedTextXPATH):
                logger.logDebugMessage("Not adding a job as already applied", MessageTypes.INFO)
                continue

            jobTitle = self.getJobTitleFromJobCardInSearchResults(jobItem)
            if not jobTitle:
                logger.logDebugMessage("Could not extract job title from job card", MessageTypes.WARNING)
                continue

            if self.isTitleBlacklisted(jobTitle):
                logger.logDebugMessage(f"Not adding job as title '{jobTitle}' is blacklisted", MessageTypes.INFO)
                continue

            companyName = self.getCompanyNameFromJobCardInSearchResults(jobItem)
            if not companyName:
                logger.logDebugMessage("Could not extract company name from job card", MessageTypes.WARNING)
                continue

            if self.isCompanyBlacklisted(companyName):
                logger.logDebugMessage(f"Not adding job as company '{companyName}' is blacklisted", MessageTypes.INFO)
                continue

            jobId = jobItem.get_attribute(constants.jobCardIdAttribute)
            if not jobId:
                logger.logDebugMessage("Could not extract job ID from job card", MessageTypes.WARNING)
                continue

            workPlaceType = self.getWorkplaceTypeFromJobCardInSearchResults(jobItem)

            jobsForVerification.append(models.JobForVerification(
                linkedinJobId = jobId.split(":")[-1],
                title = jobTitle,
                company = companyName,
                workplaceType = workPlaceType))

        return jobsForVerification


    def getCompanyNameFromJobCardInSearchResults(self, jobItem) -> Optional[str]:
        elements = jobItem.find_elements(By.CSS_SELECTOR, constants.jobCardCompanyNameCSS)
        if elements and len(elements) > 0:
            return utils.getFirstStringBeforeSeparators(elements[0].text)
        
        return None


    def getJobTitleFromJobCardInSearchResults(self, jobItem) -> Optional[str]:
        if (not self.driverHelper.exists(jobItem, By.CSS_SELECTOR, constants.jobCardTitleLinkCSS)):
            return None
        
        element = jobItem.find_element(By.CSS_SELECTOR, constants.jobCardTitleLinkCSS)
        return element.get_attribute("aria-label").strip()


    def getWorkplaceTypeFromJobCardInSearchResults(self, jobItem) -> str:
        if not self.driverHelper.exists(jobItem, By.CSS_SELECTOR, constants.jobCardDescriptionCSS):
            return ""
        
        jobCard = jobItem.find_element(By.CSS_SELECTOR, constants.jobCardDescriptionCSS)
        descriptionSpan = jobCard.find_element(By.CSS_SELECTOR, constants.spanCSS)
        workplace_type = utils.extractTextWithinParentheses(descriptionSpan.text)
        return self.verifyWorkPlaceType(workplace_type)


    # TODO Move to logger.py (after splitting utils.py)
    def getLogTextForJobProperties(self, jobProperties: models.Job, jobCounter: models.JobCounter):
        textToWrite = str(jobCounter.total) + " | " + jobProperties.title +  " | " + jobProperties.company +  " | " + jobProperties.location + " | " + jobProperties.workplace_type + " | " + jobProperties.posted_date + " | " + jobProperties.applicants_at_time_of_applying
        if self.isJobBlacklisted(company=jobProperties.company, title=jobProperties.title):
            textToWrite = textToWrite + " | " + "blacklisted"

        return textToWrite
        

    def handleJobPost(self, jobPage, jobProperties: models.Job, jobCounter: models.JobCounter):
        if not self.driverHelper.isEasyApplyButtonDisplayed():
            jobCounter.skipped_already_applied += 1
            lineToWrite = self.getLogTextForJobProperties(jobProperties, jobCounter) + " | " + "* 🥳 Already applied! Job: " + str(jobPage)
            resultFileWriter.displayWriteResults(lineToWrite)
            return jobCounter
        
        self.driverHelper.clickEasyApplyButton()
        
        if not self.driverHelper.isApplicationPopupDisplayed():
            return jobCounter
        
        # Now, the easy apply popup should be open
        if self.driverHelper.isSubmitButtonDisplayed():
            jobCounter = self.handleSubmitPage(jobPage, jobProperties, jobCounter)
        elif self.driverHelper.isNextButtonDisplayed():
            jobCounter = self.handleMultiplePages(jobPage, jobProperties, jobCounter)

        return jobCounter


    def getJobPropertiesFromJobPage(self, jobID: str) -> models.Job: 
        jobTitle = self.getJobTitleFromJobPage()
        jobCompany = self.getJobCompanyFromJobPage()
        jobLocation = ""
        jobPostedDate = ""
        numberOfApplicants = ""
        jobWorkPlaceType = self.getJobWorkPlaceTypeFromJobPage()
        jobDescription = self.getJobDescriptionFromJobPage()

        # First, find the container that holds all the elements.
        if self.driverHelper.exists(self.driverHelper.driver, By.XPATH, constants.divWithJobPagePrimaryDescriptionXPATH):
            primary_description_div = self.driver.find_element(By.XPATH, constants.divWithJobPagePrimaryDescriptionXPATH)
            jobLocation = self.getJobLocationFromJobPage(primary_description_div)
            jobPostedDate = self.getJobPostedDateFromJobPage(primary_description_div)
            numberOfApplicants = self.getNumberOfApplicantsFromJobPage(primary_description_div)
        else:
            logger.logDebugMessage("in getting primary_description_div", MessageTypes.WARNING)

        return models.Job(
            title = jobTitle,
            company = jobCompany,
            location = jobLocation,
            description = jobDescription,
            workplace_type = jobWorkPlaceType,
            posted_date = jobPostedDate,
            applicants_at_time_of_applying = numberOfApplicants,
            linkedin_job_id = jobID
        )
    

    def getJobTitleFromJobPage(self) -> str:
        jobTitle = ""

        try:
            jobTitleElement = self.driver.find_element(By.CSS_SELECTOR, constants.headerJobTitleCSS)
            jobTitle = jobTitleElement.text.strip()
        except Exception as e:
            logger.logDebugMessage("in getting jobTitle", MessageTypes.WARNING, e)

        return jobTitle
    

    def getJobCompanyFromJobPage(self) -> str:
        jobCompany = ""

        if self.driverHelper.exists(self.driverHelper.driver, By.XPATH, constants.divWithJobCompanyXPATH):
            # Inside this container, find the company name link.
            jobCompanyElement = self.driver.find_element(By.XPATH, constants.divWithJobCompanyXPATH)
            jobCompany = jobCompanyElement.text.strip()
            
        else:
            logger.logDebugMessage("in getting jobCompany card", MessageTypes.WARNING)

        return jobCompany        
    
    
    def getJobLocationFromJobPage(self, primary_description_div) -> str:
        jobLocation = ""

        try:
            jobLocationSpan = primary_description_div.find_element(By.XPATH, constants.jobLocationXPATH)
            jobLocation = jobLocationSpan.text.strip()
        except Exception as e:
            logger.logDebugMessage("in getting jobLocation", MessageTypes.WARNING, e)

        return jobLocation


    def getJobPostedDateFromJobPage(self, primary_description_div) -> str:
        jobPostedDate = ""

        try:
            primary_description_text = primary_description_div.text  # Get all text from the div
            # Regex pattern to find patterns like '6 hours ago', '2 days ago', etc.
            match = re.search(r'\b\d+\s+(seconds?|minutes?|hours?|days?|weeks?|months?)\s+ago\b', primary_description_text)
            if match:
                jobPostedDate = match.group(0)  # The whole matched text is the date

        except Exception as e:
            logger.logDebugMessage("Error in getting jobPostedDate", MessageTypes.WARNING, e)

        return jobPostedDate


    def getNumberOfApplicantsFromJobPage(self, primary_description_div) -> str:
        jobApplications = ""

        try:
            # Find all spans with the class 'tvm__text--low-emphasis'
            primaryDescriptionSpans = primary_description_div.find_elements(By.XPATH, constants.numberOfApplicantsSpanXPATH)
            # Loop through all found spans in reverse order because the number of applicants is usually the last one
            for span in reversed(primaryDescriptionSpans):
                span_text = span.text.strip()
                # Check if the text contains the keyword 'appl' (from 'applicants' or 'applications') and a number 
                if 'appl' in span_text.lower() and any(char.isdigit() for char in span_text):
                    jobApplications = span_text
                    break

        except Exception as e:
            logger.logDebugMessage("in getting jobApplications", MessageTypes.WARNING, e)

        return jobApplications


    def getJobWorkPlaceTypeFromJobPage(self) -> str:
        jobWorkPlaceType = ""

        try:
            jobWorkPlaceTypeElement = self.driver.find_element(By.XPATH, constants.jobWorkplaceTypeXPATH)
            firstSpanText = jobWorkPlaceTypeElement.text.strip().split('\n')[0]
            jobWorkPlaceType = self.verifyWorkPlaceType(firstSpanText)
        except Exception as e:
            logger.logDebugMessage("in getting jobWorkPlaceType", MessageTypes.WARNING, e)
            
        return jobWorkPlaceType
    

    # TODO Optimize: Find a faster way to verify workplace type
    def verifyWorkPlaceType(self, text: str) -> str:
        keywords = ["Remote", "On-site", "Hybrid"]
        if any(text in keyword for keyword in keywords):
            return text
        else:
            return ""


    # TODO Use jobDetail later
    def getJobDescriptionFromJobPage(self):
        jobDescription = ""

        try:
            # Directly target the div with the specific ID that contains the job description
            descriptionContainer = self.driver.find_element(By.ID, constants.jobDetailsID)
            jobDescription = descriptionContainer.text  # This should get all text within, including nested spans and divs
        except Exception as e:
            logger.logDebugMessage("in getting jobDescription: ", MessageTypes.WARNING, e)

        return jobDescription
    

    def isJobBlacklisted(self, company: str, title: str):
        is_blacklisted = self.isCompanyBlacklisted(company)
        if is_blacklisted:
            return True

        is_blacklisted = self.isTitleBlacklisted(title)
        if is_blacklisted:
            return True

        return False
    

    def isCompanyBlacklisted(self, company: str):
        return any(blacklistedCompany.strip().lower() == company.lower() for blacklistedCompany in config.blacklistCompanies)
    

    def isTitleBlacklisted(self, title: str):
        return any(blacklistedTitle.strip().lower() in title.lower() for blacklistedTitle in config.blackListTitles)

    
    def handleMultiplePages(self, jobPage, jobProperties: models.Job, jobCounter: models.JobCounter):
        while True:
            self.driverHelper.clickNextButton()
            if self.driverHelper.isQuestionsUnansweredErrorMessageDisplayed():
                # TODO Change the logic when answering to questions is implemented
                jobCounter = self.cannotApply(jobPage, jobProperties, jobCounter)
                return jobCounter
            self.handleApplicationStep(jobProperties)
            if not self.driverHelper.isNextButtonDisplayed():
                break

        if self.driverHelper.isLastApplicationStepDisplayed():
            self.driverHelper.clickReviewApplicationButton()

        if self.driverHelper.isQuestionsUnansweredErrorMessageDisplayed():
            # TODO Change the logic when answering to questions is implemented
            jobCounter = self.cannotApply(jobPage, jobProperties, jobCounter)
            return jobCounter

        jobCounter = self.handleSubmitPage(jobPage, jobProperties, jobCounter)

        return jobCounter
    

    def cannotApply(self, jobPage, jobProperties: models.Job, jobCounter: models.JobCounter) -> models.JobCounter:
        jobCounter.skipped_unanswered_questions += 1
        # TODO Instead of except, output which questions need to be answered
        lineToWrite = self.getLogTextForJobProperties(jobProperties, jobCounter) + " | " + "* 🥵 Couldn't apply to this job! Extra info needed. Link: " + str(jobPage)
        resultFileWriter.displayWriteResults(lineToWrite)

        return jobCounter
        

    def handleSubmitPage(self, jobPage, jobProperties: models.Job, jobCounter: models.JobCounter):
        followCompany = self.driver.find_element(By.CSS_SELECTOR, constants.followCheckboxCSS)
        # Use JavaScript to check the state of the checkbox
        is_followCompany_checked = self.driver.execute_script("""
            var label = arguments[0];
            var checkbox = document.getElementById('follow-company-checkbox');
            var style = window.getComputedStyle(label, '::after');
            var content = style.getPropertyValue('content');
            // Check if content is not 'none' or empty which may indicate the presence of the ::after pseudo-element
            return checkbox.checked || (content && content !== 'none' && content !== '');
        """, followCompany)
        if config.followCompanies != is_followCompany_checked:
            sleeper.interact(lambda : self.driverHelper.clickButton(followCompany))

        if self.driverHelper.isReviewApplicationStepDisplayed():
            self.driverHelper.clickSubmitApplicationButton()
            if self.driverHelper.isApplicationSubmittedDialogDisplayed():
                repository_wrapper.applied_to_job(jobProperties)
                lineToWrite = self.getLogTextForJobProperties(jobProperties, jobCounter) + " | " + "* 🥳 Just Applied to this job: " + str(jobPage)
                resultFileWriter.displayWriteResults(lineToWrite)

                jobCounter.applied += 1

        return jobCounter


    def handleApplicationStep(self, jobProperties: models.Job):
        self.driverHelper.chooseResumeIfPossible(jobProperties)
        # self.driverHelper.handleQuestions(jobProperties)


    def find_jobs_from_search_page(self) -> list[models.JobForVerification]:
        self.goToJobsSearchPage()
        jobs = self.getJobsForVerificationFromSearchPage()
        return jobs
