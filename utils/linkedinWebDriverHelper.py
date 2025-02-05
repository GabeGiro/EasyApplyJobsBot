from selenium import webdriver
from selenium.webdriver.common.by import By

import constants
import config
import models
import repository_wrapper
import utils.sleeper as sleeper
import utils.logger as logger
from utils.logger import MessageTypes


class WebDriverHelper:
    
    
    def __init__(self, driver: webdriver):
        self.driver = driver


    def checkIfLoggedIn(self):
        if self.exists(self.driver, By.CSS_SELECTOR, "img.global-nav__me-photo.evi-image.ember-view"):
            logger.logDebugMessage("✅ Logged in Linkedin.", MessageTypes.SUCCESS)
            return True
        else:
            return False
        

    def exists(self, parent, by, value):
        return len(parent.find_elements(by, value)) > 0


    def isEasyApplyButtonDisplayed(self):
        return self.exists(self.driver, By.CSS_SELECTOR, constants.easyApplyButtonCSS)


    def clickEasyApplyButton(self):
        button = self.driver.find_element(By.CSS_SELECTOR, constants.easyApplyButtonCSS)
        sleeper.interact(lambda : self.clickButton(button))


    def isApplicationPopupDisplayed(self):
        return self.exists(self.driver, By.XPATH, constants.jobApplicationHeaderXPATH)


    def __isResumePage(self):
        upload_button_present = self.exists(self.driver, By.CSS_SELECTOR, "label.jobs-document-upload__upload-button")
        resume_container_present = self.exists(self.driver, By.CSS_SELECTOR, "div.jobs-document-upload-redesign-card__container")
        return upload_button_present and resume_container_present
    

    def chooseResumeIfPossible(self, jobProperties: models.Job):
        if self.__isResumePage():
            sleeper.interact(lambda : self.__clickIfExists(By.CSS_SELECTOR, "button[aria-label='Show more resumes']"))

            # Find all CV container elements
            cv_containers = self.driver.find_elements(By.CSS_SELECTOR, ".jobs-document-upload-redesign-card__container")

            # Loop through the elements to find the desired CV
            for container in cv_containers:
                cv_name_element = container.find_element(By.CLASS_NAME, "jobs-document-upload-redesign-card__file-name")
                
                if config.distinctCVKeyword[0] in cv_name_element.text:
                    # Check if CV is already selected
                    if 'jobs-document-upload-redesign-card__container--selected' not in container.get_attribute('class'):
                        sleeper.interact(lambda : self.clickButton(cv_name_element))

                    # Update the backend to save the selected CV
                    repository_wrapper.attached_resume_to_job(jobProperties, cv_name_element.text)
                    # exit the loop once the desired CV is found and selected
                    break  

    def isNextButtonDisplayed(self):
        return self.exists(self.driver, By.CSS_SELECTOR, constants.nextPageButtonCSS)


    def clickNextButton(self):
        button = self.driver.find_element(By.CSS_SELECTOR, constants.nextPageButtonCSS)
        sleeper.interact(lambda : self.clickButton(button))


    def isLastApplicationStepDisplayed(self):
        return self.exists(self.driver, By.CSS_SELECTOR, constants.reviewApplicationButtonCSS)


    def extract_percentage(self):
        if not self.exists(self.driver, By.XPATH, constants.multiplePagePercentageXPATH):
            logger.logDebugMessage("Could not find percentage element", MessageTypes.WARNING)
            return None

        percentageElement = self.driver.find_element(By.XPATH, constants.multiplePagePercentageXPATH)
        comPercentage = percentageElement.get_attribute("value")
        
        if not comPercentage or not comPercentage.replace('.', '').isdigit():
            logger.logDebugMessage(f"Invalid percentage value: {comPercentage}", MessageTypes.ERROR)
            return None

        percentage = float(comPercentage)
        if percentage <= 0:
            logger.logDebugMessage("Percentage must be positive", MessageTypes.ERROR)
            return None
        
        return percentage
    

    def clickReviewApplicationButton(self):
        button = self.driver.find_element(By.CSS_SELECTOR, constants.reviewApplicationButtonCSS)
        sleeper.interact(lambda : self.clickButton(button))


    def isReviewApplicationStepDisplayed(self):
        return self.exists(self.driver, By.CSS_SELECTOR, constants.submitApplicationButtonCSS)


    def isSubmitButtonDisplayed(self):
        return self.exists(self.driver, By.CSS_SELECTOR, constants.submitApplicationButtonCSS)


    def clickSubmitApplicationButton(self):
        button = self.driver.find_element(By.CSS_SELECTOR, constants.submitApplicationButtonCSS)
        sleeper.interact(lambda : self.clickButton(button))


    def isApplicationSubmittedDialogDisplayed(self):
        dialog = self.driver.find_element(By.CSS_SELECTOR, "div[data-test-modal][role='dialog']")
        dismiss_button_present = self.exists(dialog, By.CSS_SELECTOR, "button[aria-label='Dismiss']")
        return dismiss_button_present


    def isQuestionsUnansweredErrorMessageDisplayed(self):
        return self.exists(self.driver, By.CSS_SELECTOR, constants.errorMessageForNecessaryFiledCSS)


    def getJobsListFromSearchPage(self):
        return self.driver.find_elements(By.CSS_SELECTOR, constants.jobCardContainerCSS)


    def handleQuestions(self, jobProperties: models.Job):
        if self.exists(self.driver, By.CSS_SELECTOR, "div.pb4"):
            # Locate the div that contains all the questions
            questionsContainer = self.driver.find_element(By.CSS_SELECTOR, "div.pb4")

            if self.exists(questionsContainer, By.CSS_SELECTOR, "div.jobs-easy-apply-form-section__grouping"):
                # Find all question groups within that div
                questionGroups = questionsContainer.find_elements(By.CSS_SELECTOR, "div.jobs-easy-apply-form-section__grouping")

                # Iterate through each question group
                for group in questionGroups:
                    # TODO Next commented code is to handle city selection and other dropdowns
                    """  
                    # Find the element (assuming you have a way to locate this div, here I'm using a common class name they might share)
                    div_element = self.driver.find_element(By.CLASS_NAME, "common-class-name")

                    # Check for the specific data-test attribute
                    if div_element.get_attribute("data-test-single-typeahead-entity-form-component") is not None:
                        # Handle the first type of div
                        print("This is the first type of div with data-test-single-typeahead-entity-form-component")

                    elif div_element.get_attribute("data-test-single-line-text-form-component") is not None:
                        # Handle the second type of div
                        print("This is the second type of div with data-test-single-line-text-form-component")

                    else:
                        # Handle the case where the div doesn't match either type
                        print("The div doesn't match either specified type")
                    """

                    if self.exists(group, By.CSS_SELECTOR, "label.artdeco-text-input--label"):
                        # Find the label for the question within the group
                        questionLabel = group.find_element(By.CSS_SELECTOR, "label.artdeco-text-input--label").text
                        
                        # Determine the type of question and call the appropriate handler
                        if self.exists(group, By.CSS_SELECTOR, "input.artdeco-text-input--input"):
                            self.__handleTextInput(group, questionLabel, By.CSS_SELECTOR, "input.artdeco-text-input--input")
                        elif self.exists(group, By.CSS_SELECTOR, "textarea"):
                            self.__handleTextInput(group, questionLabel, By.CSS_SELECTOR, "textarea")
                        elif self.exists(group, By.CSS_SELECTOR, "input[type='radio']"):
                            self.__handleRadioInput(group, questionLabel, By.CSS_SELECTOR, "input[type='radio']")
                        else:
                            self.__logUnhandledQuestion(questionLabel)


    def __handleTextInput(self, group, questionLabel, by, value):
        # Locate the input element  
        inputElement = group.find_element(by, value)

        # Retrieve the value of the input element
        inputValue = inputElement.get_attribute('value')

        # Check if the input element is empty
        if inputValue == '':
            # TODO Check the backend for answers

            # TODO If there is an answer for this question, fill it in
            # If you want to fill the input
            # question_input.send_keys("Your answer here") then sleep
            # If no answers are found, move to the next step (backend should handle saving unanswered questions)
            if config.displayWarnings:
                logger.logDebugMessage(f"The input for '{questionLabel}' is empty.", MessageTypes.WARNING)
        else:
            # TODO Save answers to the backend if they are not already saved
            if config.displayWarnings:
                logger.logDebugMessage(f"The input for '{questionLabel}' has the following value: {inputValue}", MessageTypes.WARNING)


    def __handleRadioInput(self, group, questionLabel, by, value):
        # Check if it's a radio selector question
        radioInputs = group.find_elements(by, value)
        for radioInput in radioInputs:
            # Retrieve the associated label
            label = radioInput.find_element(By.XPATH, "./following-sibling::label").text
            # TODO Check the backend for answers. If there is an answer for this question, fill it in
            # Check or uncheck based on some condition
            # if "desired option" in label:
            #     logger.logDebugMessage(f"Selecting option: {label}", MessageTypes.WARNING)
            #     radio_input.click()  # Select the radio button if it's the desired option then sleep


    def __logUnhandledQuestion(self, questionLabel):
        # Log or print the unhandled question
        logger.logDebugMessage(f"Unhandled question: {questionLabel}", MessageTypes.ERROR)


    def __clickIfExists(self, by, selector):
        if self.exists(self.driver, by, selector):
            clickableElement = self.driver.find_element(by, selector)
            self.clickButton(clickableElement)


    def clickButton(self, button):
        try:
            button.click()
        except Exception as e:
            # If click fails, use JavaScript to click on the button
            self.driver.execute_script("arguments[0].click();", button)