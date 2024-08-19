import random
import time

import constants


def sleepInBetweenActions(
    bottom: int = constants.botSleepInBetweenActionsBottom,
    top: int = constants.botSleepInBetweenActionsTop,
):
    time.sleep(random.uniform(bottom, top))


def sleepInBetweenBatches(
    currentBatch: int,
    bottom: int = constants.botSleepInBetweenBatchesBottom,
    top: int = constants.botSleepInBetweenBatchesTop,
):
    if currentBatch % constants.batchSize == 0:
        time.sleep(random.uniform(bottom, top))
