import time
from linkedin import Linkedin
import utils.logger as logger
from utils.logger import MessageTypes


start = time.time()
Linkedin().startApplying()
end = time.time()
logger.logDebugMessage("---Took: " + str(round((time.time() - start)/60)) + " minute(s).")
