import config
import utils.utils as utils
import traceback
from enum import Enum


class MessageTypes(Enum):
    INFO = 1
    WARNING = 2
    ERROR = 3
    SUCCESS = 4


def logDebugMessage(message, messageType = MessageTypes.INFO, exception = Exception(), displayTraceback = False):
    if (config.displayWarnings):
        match messageType:
            case MessageTypes.INFO:
                __prBlue(f"ℹ️ {message}")
            case MessageTypes.WARNING:
                __prYellow(f"⚠️ Warning ⚠️ {message}: {str(exception)[0:100]}")
            case MessageTypes.ERROR:
                __prRed(f"❌ Error ❌ {message}: {str(exception)[0:200]}")
            case MessageTypes.SUCCESS:
                __prGreen(f"✅ {message}")

        if (displayTraceback):
            traceback.print_exc()


def __prRed(prt):
    print(f"\033[91m{prt}\033[00m")


def __prGreen(prt):
    print(f"\033[92m{prt}\033[00m")


def __prYellow(prt):
    print(f"\033[93m{prt}\033[00m")


def __prBlue(prt):
    print(f"\033[94m{prt}\033[00m")
