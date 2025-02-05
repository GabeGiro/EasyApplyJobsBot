import utils.utils as utils, models
import utils.logger as logger
from utils.logger import MessageTypes
from typing import List
from dotenv import load_dotenv

initialized = False
backend_api = None


def init():
    global initialized, backend_api
    logger.logDebugMessage("Initializing repository wrapper...")
    initialized, backend_api = import_backend_module()


def import_backend_module():
    try:
        result = load_dotenv(".env")
        print(f"Is .env file loaded = {result}")
        
        from frontend.utils import (
            api as backend_api,  # Change this line with your backend module
        )
        logger.logDebugMessage(f"Successfully imported backend module", MessageTypes.SUCCESS)

        return True, backend_api
    
    except ImportError as e:
        logger.logDebugMessage(f"Could not import backend module: {e}", MessageTypes.WARNING)
        return False, None
    

def verify_jobs(jobs: models.JobForVerification) -> List[models.JobForVerification]:
    if initialized:
        try:
            logger.logDebugMessage(f"Verifying jobs: {jobs}")
            jobs = backend_api.verify_jobs(jobs)
        except Exception as e:
            logger.logDebugMessage(f"Error verifying jobs: {e}", MessageTypes.ERROR)

    return jobs
    

def update_job(job: models.Job):
    if initialized:
        try:
            logger.logDebugMessage(f"Updating job: {job}")
            job = backend_api.update_job_with_job_properties(job)
        except Exception as e:
            logger.logDebugMessage(f"Error updating job: {e}", MessageTypes.ERROR)

    return job

def attached_resume_to_job(job: models.Job, resume: str):
    if initialized:
        try:
            logger.logDebugMessage(f"Attaching resume to job: {job}")
            backend_api.attached_resume_to_job(job.linkedin_job_id, resume)
        except Exception as e:
            logger.logDebugMessage(f"Error attaching resume to job: {e}", MessageTypes.ERROR)

def get_answer_by_question(question):
    if initialized:
        try:
            logger.logDebugMessage(f"Getting answer for question: {question}")
            # TODO: Implement this
        except Exception as e:
            logger.logDebugMessage(f"Error getting answer for question: {e}", MessageTypes.ERROR)


def post_question(question):
    if initialized:
        try:
            logger.logDebugMessage(f"Posting question: {question} with answer:")
            # TODO: Implement this
        except Exception as e:
            logger.logDebugMessage(f"Error posting question: {e}", MessageTypes.ERROR)


def applied_to_job(job: models.Job):
    if initialized:
        try:
            logger.logDebugMessage(f"Marking job as applied: {job}")
            backend_api.applied_to_job(job.linkedin_job_id)
        except Exception as e:
            logger.logDebugMessage(f"Error marking job as applied: {e}", MessageTypes.ERROR)
