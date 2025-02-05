import time
import random
import constants


def interact(action):
    action()
    __sleepInBetweenActions()


def __sleepInBetweenActions(bottom: int = constants.botSleepInBetweenActionsBottom, top: int = constants.botSleepInBetweenActionsTop):
    time.sleep(random.uniform(bottom, top))


def sleepInBetweenBatches(currentBatch: int, bottom: int = constants.botSleepInBetweenBatchesBottom, top: int = constants.botSleepInBetweenBatchesTop):
    if (currentBatch % constants.batchSize == 0):
        time.sleep(random.uniform(bottom, top))