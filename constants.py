websiteUrl = "www.automated-bots.com"
contactUrl = "https://www.automated-bots.com/contact"

searchJobsUrl = "https://www.linkedin.com/jobs/search/"
searchEasyApplyJobsUrl = "https://www.linkedin.com/jobs/search/?f_AL=true"
angelCoUrl = "https://angel.co/login"
globalLogicUrl = "https://www.globallogic.com/career-search-page/"

jobsPerPage = 25

fast = 2
medium = 3
slow = 5 

botSleepInBetweenActionsBottom = 4
botSleepInBetweenActionsTop = 12

botSleepInBetweenBatchesBottom = 10
botSleepInBetweenBatchesTop = 70
batchSize = 10

botSleepInBetweenSearchesBottom = 60
botSleepInBetweenSearchesTop = 180


# Webdriver Elements 
jobsPageUrl = "https://www.linkedin.com/jobs"
testJobUrl = "https://www.linkedin.com/jobs/search/?currentJobId=3577461385&distance=25&f_AL=true&f_E=2&f_JT=F%2CP%2CC&f_SB2=3&f_WT=1%2C2%2C3&geoId=102221843&keywords=frontend"
testPageUrl = testJobUrl +"&start="+ str(2)


# Xpath Selectors
offersPerPageXPATH = "//li[@data-occludable-job-id]"
jobsPageCareerClassXPATH = "//div[contains(@class, 'careers')]"
totalJobsXPATH = "//small"
jobApplicationHeaderXPATH = "//h2[@id='jobs-apply-header']"
multiplePagePercentageXPATH = "//progress[contains(@class, 'artdeco-completeness-meter-linear__progress-element')]"

# CSS Selectors
easyApplyButtonCSS = "button[aria-label*='Easy Apply']"
nextPageButtonCSS = "button[aria-label='Continue to next step']"
reviewApplicationButtonCSS = "button[aria-label*='Review']"
submitApplicationButtonCSS = "button[aria-label='Submit application']"
errorMessageForNecessaryFiledCSS = "div.artdeco-inline-feedback.artdeco-inline-feedback--error[data-test-form-element-error-messages]"


# TO DO ADD OTHER PRINT CONSTANTS

# Linkedin Constants
## Job Title Constants
job_title_codes = {
    'Android Developer': "25166",
    'Mobile Engineer': "7110",
    'Mobile Application Developer': "18930",
    'Scrum Master': "7586",
    'Chief Technology Officer': "153",
    'Director of Technology': "382",
    'Head of Information Technology': "688",
    'Technical Director': "200",
    'Co-Founder': "103",
    'Data Analyst': "340",
    'Business Data Analyst': "6358",
    'Business Intelligence Consultant': "733",
    'Business Intelligence Analyst': "2336",
    'Data Specialist': "1547",
    'Data Scientist': "25190",
    'Data Engineer': "2732",
    'Machine Learning Engineer': "25206",
    'Artificial Intelligence Engineer': "30128",
    'Python Developer': "25169",
}

APPLIED_TEXT_XPATH = ".//*[contains(text(), 'Applied')]"
JOB_CARD_COMPANY_NAME_CSS = "[data-tracking-control-name='public_jobs_company_name']"
JOB_CARD_SUBTITLE_CSS = "[class*='base-card__subtitle']"
JOB_CARD_METADATA_CSS = "[class*='job-card-container__metadata']"
JOB_CARD_COMPANY_CSS = "[class*='company-name']"
JOB_CARD_TITLE_LINK_CSS = "a[class*='job-card-list__title']"
JOB_CARD_TITLE_HEADING_CSS = "h3[class*='job-card-list__title']"
JOB_CARD_BASE_TITLE_CSS = "[class*='base-card__title']"
JOB_CARD_TITLE_LABEL_CSS = "[aria-label*='job title']"
JOB_CARD_DESCRIPTION_CSS = "span.job-card-container__primary-description"
