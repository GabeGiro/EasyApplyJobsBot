import math
import os
import time

import config
import constants
from selenium import webdriver

from utils.sleeper import sleepInBetweenActions
from utils.logger import prRed


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
    sleepInBetweenActions()