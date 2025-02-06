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
            resultFileWriter.create_directory('data')
            resultFileWriter.create_directory('data/tests')
               

            id = self.id()
            class_name = id.split('.')[0]
            method_name = id.split('.')[-1]

            test_directory = resultFileWriter.join_paths('data/tests', class_name, method_name)
            
            resultFileWriter.create_directory(test_directory)
            
            screenshot_path = resultFileWriter.join_paths(test_directory, "screenshot.png")
            html_path = resultFileWriter.join_paths(test_directory, "page.html")

            # Capture screenshot
            resultFileWriter.capture_screenshot(driver, screenshot_path)
            
            # Capture HTML content
            resultFileWriter.capture_html(driver, html_path)

        except WebDriverException as e:
            print(f"Failed to capture screenshot or HTML: {e}")

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
