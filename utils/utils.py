import math
import os
import re
from selenium import webdriver

import config
import constants


def chromeBrowserOptions():
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--disable-extensions")
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    if(config.headless):
        options.add_argument("--headless")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option('useAutomationExtension', False)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    if(len(config.chromeProfilePath)>0):
        initialPath = config.chromeProfilePath[0:config.chromeProfilePath.rfind("/")]
        profileDir = config.chromeProfilePath[config.chromeProfilePath.rfind("/")+1:]
        options.add_argument('--user-data-dir=' + initialPath)
        options.add_argument("--profile-directory=" + profileDir)
    else:
        # options.add_argument("--incognito")
        # this is for running in a docker container
        user_data_dir = os.environ.get('CHROME_USER_DATA_DIR', '/home/user/chrome_data')
        options.add_argument(f'--user-data-dir={user_data_dir}')
    return options


def jobsToPages(numOfJobs: str) -> int:
  number_of_pages = 1

  if (' ' in numOfJobs):
    spaceIndex = numOfJobs.index(' ')
    totalJobs = (numOfJobs[0:spaceIndex])
    totalJobs_int = int(totalJobs.replace(',', ''))
    number_of_pages = math.ceil(totalJobs_int/constants.jobsPerPage)
    if (number_of_pages > 40 ): number_of_pages = 40

  else:
      number_of_pages = int(numOfJobs)

  return number_of_pages


def extractTextWithinParentheses(text):
    # Pattern to match text within parentheses
    pattern = r"\((.*?)\)"
    match = re.search(pattern, text)
    
    if match:
        # Return the content within the first set of parentheses
        return match.group(1)  # `group(1)` returns the content within the parentheses
    else:
        return ""


def getFirstStringBeforeSeparators(text: str, separators=['·', '(', '-', '|']) -> str:
    if not text:
        return ""
        
    for separator in separators:
        if separator in text:
            text = text.split(separator)[0]
    
    return text.strip()


def progressMatchesExpectedApplicationPage(step: int, numberOfSteps, progress: float):
    return math.isclose(progress, (step / numberOfSteps) * 100, rel_tol=0.001) # TODO Try without is close, but just equals