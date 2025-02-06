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

numberOfDefaultPagesInApplication = 2


# Webdriver Elements 
jobsPageUrl = "https://www.linkedin.com/jobs"
testJobUrl = "https://www.linkedin.com/jobs/search/?currentJobId=3577461385&distance=25&f_AL=true&f_E=2&f_JT=F%2CP%2CC&f_SB2=3&f_WT=1%2C2%2C3&geoId=102221843&keywords=frontend"
testPageUrl = testJobUrl +"&start="+ str(2)


# Class Name Selectors
resumeNameElementClassName = "jobs-document-upload-redesign-card__file-name"


# CSS Selectors
buttonDismissCSS = "button[aria-label='Dismiss']"
buttonDocumentUploadCSS = "label.jobs-document-upload__upload-button"
buttonEasyApplyCSS = "button[aria-label*='Easy Apply']"
buttonNextPageCSS = "button[aria-label='Continue to next step']"
buttonReviewApplicationCSS = "button[aria-label*='Review']"
buttonShowMoreDocumentsCSS = "button[aria-label='Show more resumes']"
buttonSubmitApplicationCSS = "button[aria-label='Submit application']"

dialogApplicationSubmittedCSS = "div[data-test-modal][role='dialog']"

errorMessageForNecessaryFiledCSS = "div.artdeco-inline-feedback.artdeco-inline-feedback--error[data-test-form-element-error-messages]"

followCheckboxCSS = "label[for='follow-company-checkbox']"

jobCardContainerCSS = "li[data-occludable-job-id]"
jobCardCompanyCSS = "[class*='company-name']"
jobCardCompanyNameCSS = "[data-tracking-control-name='public_jobs_company_name']"
jobCardDescriptionCSS = "ul.job-card-container__metadata-wrapper"
jobCardIdAttribute = "data-occludable-job-id"
jobCardMetadataCSS = "[class*='job-card-container__metadata']"
jobCardSubtitleCSS = "[class*='base-card__subtitle']"

jobCardTitleLinkCSS = "a.job-card-list__title--link"
# TODO Try adding other selectors to increase the number of job titles found
# jobCardTitleLinkCSS = "a[class*='job-card-list__title']"
# jobCardTitleHeadingCSS = "h3[class*='job-card-list__title']"
# jobCardBaseTitleCSS = "[class*='base-card__title']"
# jobCardTitleLabelCSS = "[aria-label*='job title']"

profilePhotoCSS = "img.global-nav__me-photo.evi-image.ember-view"

resumeContainerCSS = ".jobs-document-upload-redesign-card__container"

spanCSS = "span"


# Xpath Selectors
offersPerPageXPATH = "//li[@data-occludable-job-id]"
jobsPageCareerClassXPATH = "//div[contains(@class, 'careers')]"
totalJobsXPATH = "//small"
jobApplicationHeaderXPATH = "//h2[@id='jobs-apply-header']"
multiplePagePercentageXPATH = """//progress[contains(@class, 'artdeco-completeness-meter-linear__progress-element')]"""
appliedTextXPATH = ".//*[contains(text(), 'Applied')]"


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

