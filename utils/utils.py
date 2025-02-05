import math
import os
import random
import time
import traceback
import re
from enum import Enum
from typing import List
from selenium import webdriver
from selenium.common.exceptions import WebDriverException

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


def prRed(prt):
    print(f"\033[91m{prt}\033[00m")


def prGreen(prt):
    print(f"\033[92m{prt}\033[00m")


def prYellow(prt):
    print(f"\033[93m{prt}\033[00m")


def prBlue(prt):
    print(f"\033[94m{prt}\033[00m")


class MessageTypes(Enum):
    INFO = 1
    WARNING = 2
    ERROR = 3
    SUCCESS = 4


def printInfoMes(bot:str):
    prYellow("ℹ️ " +bot+ " is starting soon... ")


def logDebugMessage(message, messageType=MessageTypes.INFO, exception=Exception(), displayTraceback = False):
    if (config.displayWarnings):
        match messageType:
            case MessageTypes.INFO:
                prBlue(f"ℹ️ {message}")
            case MessageTypes.WARNING:
                prYellow(f"⚠️ Warning ⚠️ {message}: {str(exception)[0:100]}")
            case MessageTypes.ERROR:
                prRed(f"❌ Error ❌ {message}: {str(exception)[0:100]}")
            case MessageTypes.SUCCESS:
                prGreen(f"✅ {message}")

        if (displayTraceback):
            traceback.print_exc()


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


def urlToKeywords(url: str) -> List[str]:
    keywordUrl = url[url.index("keywords=")+9:]
    keyword = keywordUrl[0:keywordUrl.index("&") ] 
    locationUrl = url[url.index("location=")+9:]
    location = locationUrl[0:locationUrl.index("&") ] 
    return [keyword,location]


def writeResults(text: str):
    timeStr = time.strftime("%Y%m%d")
    directory = "data"
    fileName = "Applied Jobs DATA - " + timeStr + ".txt"
    filePath = os.path.join(directory, fileName)

    try:
        os.makedirs(directory, exist_ok=True)  # Ensure the 'data' directory exists.

        # Open the file for reading and writing ('r+' opens the file for both)
        with open(filePath, 'r+', encoding="utf-8") as file:
            lines = []
            for line in file:
                if "----" not in line:
                    lines.append(line)
            file.seek(0)  # Go back to the start of the file
            file.truncate()  # Clear the file
            file.write("---- Applied Jobs Data ---- created at: " + timeStr + "\n")
            file.write("---- Number | Job Title | Company | Location | Work Place | Posted Date | Applications | Result " + "\n")
            for line in lines:
                file.write(line)
            file.write(text + "\n")
    except FileNotFoundError:
        with open(filePath, 'w', encoding="utf-8") as f:
            f.write("---- Applied Jobs Data ---- created at: " + timeStr + "\n")
            f.write("---- Number | Job Title | Company | Location | Work Place | Posted Date | Applications | Result " + "\n")
            f.write(text + "\n")
    except Exception as e:
        prRed(f"❌ Error in writeResults: {e}")  # Assuming prRed is a function to print errors in red color


# def writeResults(text: str):
#     timeStr = time.strftime("%Y%m%d")
#     fileName = "Applied Jobs DATA - " +timeStr + ".txt"
#     try:
#         with open("data/" +fileName, encoding="utf-8" ) as file:
#             lines = []
#             for line in file:
#                 if "----" not in line:
#                     lines.append(line)
                
#         with open("data/" +fileName, 'w' ,encoding="utf-8") as f:
#             f.write("---- Applied Jobs Data ---- created at: " +timeStr+ "\n" )
#             f.write("---- Number | Job Title | Company | Location | Work Place | Posted Date | Applications | Result "   +"\n" )
#             for line in lines: 
#                 f.write(line)
#             f.write(text+ "\n")
            
#     except:
#         with open("data/" +fileName, 'w', encoding="utf-8") as f:
#             f.write("---- Applied Jobs Data ---- created at: " +timeStr+ "\n" )
#             f.write("---- Number | Job Title | Company | Location | Work Place | Posted Date | Applications | Result "   +"\n" )

#             f.write(text+ "\n")


def interact(action):
    action()
    __sleepInBetweenActions()


def __sleepInBetweenActions(bottom: int = constants.botSleepInBetweenActionsBottom, top: int = constants.botSleepInBetweenActionsTop):
    time.sleep(random.uniform(bottom, top))


def sleepInBetweenBatches(currentBatch: int, bottom: int = constants.botSleepInBetweenBatchesBottom, top: int = constants.botSleepInBetweenBatchesTop):
    if (currentBatch % constants.batchSize == 0):
        time.sleep(random.uniform(bottom, top))


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