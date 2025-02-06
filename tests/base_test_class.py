import unittest
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import os

class BaseTestCase(unittest.TestCase):

    def tearDown(self, driver: webdriver.Chrome):
        """Capture screenshot and HTML content if the test fails."""

        test_exceptions = self._outcome.result.errors
        test_failures = self._outcome.result.failures
        if any(error for (_, error) in test_exceptions) or test_failures:
            self.capture_test_failure_info(driver)

        super().tearDown()
        # driver.quit()

    # TODO Move this to file.py
    def capture_test_failure_info(self, driver: webdriver.Chrome):
        """Capture screenshots and HTML content for debugging."""

        try:
            if not os.path.exists('data'):
                os.makedirs('data')

            if not os.path.exists('data/tests'):
                os.makedirs('data/tests')

            id = self.id()
            class_name = id.split('.')[0]
            method_name = id.split('.')[-1]

            test_directory = os.path.join('data/tests', class_name, method_name)
            
            if not os.path.exists(test_directory):
                os.makedirs(test_directory)
            
            screenshot_path = os.path.join(test_directory, "screenshot.png")
            html_path = os.path.join(test_directory, "page.html")

            # Capture screenshot
            driver.save_screenshot(screenshot_path)
            
            # Capture HTML content
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(driver.page_source)

        except WebDriverException as e:
            print(f"Failed to capture screenshot or HTML: {e}")

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
