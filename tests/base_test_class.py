import unittest
from selenium import webdriver
from selenium.common.exceptions import WebDriverException

import utils.file as resultFileWriter


class BaseTestCase(unittest.TestCase):

    def tearDown(self, driver: webdriver.Chrome):
        """Capture screenshot and HTML content if the test fails."""

        test_exceptions = self._outcome.result.errors
        test_failures = self._outcome.result.failures
        if any(error for (_, error) in test_exceptions) or test_failures:
            self.capture_test_failure_info(driver)

        super().tearDown()
        # driver.quit()

    
    def capture_test_failure_info(self, driver: webdriver.Chrome):
        """Capture screenshots and HTML content for debugging."""

        try:
            resultFileWriter.createDirectory('data')
            resultFileWriter.createDirectory('data/tests')
               

            id = self.id()
            className = id.split('.')[0]
            methodName = id.split('.')[-1]

            testDirectory = resultFileWriter.joinPaths('data/tests', className, methodName)
            
            resultFileWriter.createDirectory(testDirectory)
            
            screenshotPath = resultFileWriter.joinPaths(testDirectory, "screenshot.png")
            htmlPath = resultFileWriter.joinPaths(testDirectory, "page.html")

            # Capture screenshot
            resultFileWriter.captureScreenshot(driver, screenshotPath)
            
            # Capture HTML content
            resultFileWriter.captureHtml(driver, htmlPath)

        except WebDriverException as e:
            print(f"Failed to capture screenshot or HTML: {e}")

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
