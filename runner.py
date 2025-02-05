import time
from linkedin import Linkedin
from utils.utils import prYellow


start = time.time()
Linkedin().startApplying()
end = time.time()
prYellow("---Took: " + str(round((time.time() - start)/60)) + " minute(s).")
