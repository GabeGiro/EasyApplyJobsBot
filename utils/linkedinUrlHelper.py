from typing import List

import config
import constants


def getGeneralSearchUrl():
    return constants.searchJobsUrl


def getEasyApplySearchUrl():
    return constants.searchEasyApplyJobsUrl


def urlToKeywords(url: str) -> List[str]:
    keywordUrl = url[url.index("keywords=") + 9:]
    keyword = keywordUrl[0 : keywordUrl.index("&")] 
    locationUrl = url[url.index("location=") + 9:]
    location = locationUrl[0 : locationUrl.index("&")] 
    return [keyword, location]


def generateSearchUrls():
    urls = []
    for location in config.location:
        for keyword in config.keywords:
            url = constants.searchJobsUrl + "?f_AL=true&keywords=" + keyword + jobType() + remote() + checkJobLocation(location) + jobExp() + datePosted() + jobTitle() + salary() + sortBy()
            urls.append(url)
    return urls


def checkJobLocation(job):
    jobLoc = "&location=" + job
    match job.casefold():
        case "asia":
            jobLoc += "&geoId=102393603"
        case "europe":
            jobLoc += "&geoId=100506914"
        case "northamerica":
            jobLoc += "&geoId=102221843&"
        case "southamerica":
            jobLoc +=  "&geoId=104514572"
        case "australia":
            jobLoc +=  "&geoId=101452733"
        case "africa":
            jobLoc += "&geoId=103537801"
        case "sweden":
            jobLoc += "&geoId=105117694"
        case "norway":
            jobLoc += "&geoId=103819153"
        case "germany":
            jobLoc += "&geoId=101282230"
        case "switzerland":
            jobLoc += "&geoId=106693272"
        case "new york":
            jobLoc += "&geoId=105080838"

    return jobLoc


def jobExp():
    jobExperienceArray = config.experienceLevels
    firstJobExperience = jobExperienceArray[0]
    jobExperience = ""
    match firstJobExperience:
        case "Internship":
            jobExperience = "&f_E=1"
        case "Entry level":
            jobExperience = "&f_E=2"
        case "Associate":
            jobExperience = "&f_E=3"
        case "Mid-Senior level":
            jobExperience = "&f_E=4"
        case "Director":
            jobExperience = "&f_E=5"
        case "Executive":
            jobExperience = "&f_E=6"
    for index in range (1,len(jobExperienceArray)):
        match jobExperienceArray[index]:
            case "Internship":
                jobExperience += "%2C1"
            case "Entry level":
                jobExperience +="%2C2"
            case "Associate":
                jobExperience +="%2C3"
            case "Mid-Senior level":
                jobExperience += "%2C4"
            case "Director":
                jobExperience += "%2C5"
            case "Executive":
                jobExperience  +="%2C6"

    return jobExperience


def datePosted():
    datePosted = ""
    match config.datePosted[0]:
        case "Any Time":
            datePosted = ""
        case "Past Month":
            datePosted = "&f_TPR=r2592000&"
        case "Past Week":
            datePosted = "&f_TPR=r604800&"
        case "Past 24 hours":
            datePosted = "&f_TPR=r86400&"
    return datePosted


def jobType():
    jobTypeArray = config.jobType
    firstjobType = jobTypeArray[0]
    jobType = ""
    match firstjobType:
        case "Full-time":
            jobType = "&f_JT=F"
        case "Part-time":
            jobType = "&f_JT=P"
        case "Contract":
            jobType = "&f_JT=C"
        case "Temporary":
            jobType = "&f_JT=T"
        case "Volunteer":
            jobType = "&f_JT=V"
        case "Intership":
            jobType = "&f_JT=I"
        case "Other":
            jobType = "&f_JT=O"
    for index in range (1,len(jobTypeArray)):
        match jobTypeArray[index]:
            case "Full-time":
                jobType += "%2CF"
            case "Part-time":
                jobType +="%2CP"
            case "Contract":
                jobType +="%2CC"
            case "Temporary":
                jobType += "%2CT"
            case "Volunteer":
                jobType += "%2CV"
            case "Intership":
                jobType  +="%2CI"
            case "Other":
                jobType  +="%2CO"
    jobType += "&"
    return jobType


def remote():
    remoteArray = config.remote
    firstJobRemote = remoteArray[0]
    jobRemote = ""
    match firstJobRemote:
        case "On-site":
            jobRemote = "f_WT=1"
        case "Remote":
            jobRemote = "f_WT=2"
        case "Hybrid":
            jobRemote = "f_WT=3"
    for index in range (1,len(remoteArray)):
        match remoteArray[index]:
            case "On-site":
                jobRemote += "%2C1"
            case "Remote":
                jobRemote += "%2C2"
            case "Hybrid":
                jobRemote += "%2C3"

    return jobRemote


def jobTitle():
    jobTitleArray = config.jobTitles
    
    # Ensure we have at least one job title to process
    if not jobTitleArray:
        return ""

    # Use the first job title for the initial job title parameter
    initial_code = constants.job_title_codes.get(jobTitleArray[0])
    if initial_code:
        jobTitle = f"f_T={initial_code}"
    else:
        return ""  # If the first job title isn't recognized, return an empty string or handle error appropriately
    
    # Process subsequent job titles
    for title in jobTitleArray[1:]:
        code = constants.job_title_codes.get(title)
        if code:
            jobTitle += f"%2C{code}"

    jobTitle += "&"
    return jobTitle


def salary():
    salary = ""
    match config.salary:
        case "$40,000+":
            salary = "f_SB2=1&"
        case "$60,000+":
            salary = "f_SB2=2&"
        case "$80,000+":
            salary = "f_SB2=3&"
        case "$100,000+":
            salary = "f_SB2=4&"
        case "$120,000+":
            salary = "f_SB2=5&"
        case "$140,000+":
            salary = "f_SB2=6&"
        case "$160,000+":
            salary = "f_SB2=7&"    
        case "$180,000+":
            salary = "f_SB2=8&"    
        case "$200,000+":
            salary = "f_SB2=9&"                  
    return salary


def sortBy():
    sortBy = ""
    match config.sort[0]:
        case "Recent":
            sortBy = "sortBy=DD"
        case "Relevent":
            sortBy = "sortBy=R"                
    return sortBy