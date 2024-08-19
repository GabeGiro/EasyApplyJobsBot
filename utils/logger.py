import traceback
from enum import Enum

import config


class MessageTypes(Enum):
    INFO = 1
    WARNING = 2
    ERROR = 3
    SUCCESS = 4


def prRed(prt):
    print(f"\033[91m{prt}\033[00m")


def prGreen(prt):
    print(f"\033[92m{prt}\033[00m")


def prYellow(prt):
    print(f"\033[93m{prt}\033[00m")


def prBlue(prt):
    print(f"\033[94m{prt}\033[00m")


def printInfoMes(bot: str):
    prYellow("ℹ️ " + bot + " is starting soon... ")


def logDebugMessage(
    message,
    messageType=MessageTypes.INFO,
    exception=Exception(),
    displayTraceback=False,
):
    if config.displayWarnings:
        match messageType:
            case MessageTypes.INFO:
                prBlue(f"ℹ️ {message}")
            case MessageTypes.WARNING:
                prYellow(f"⚠️ Warning ⚠️ {message}: {str(exception)[0:100]}")
            case MessageTypes.ERROR:
                prRed(f"❌ Error ❌ {message}: {str(exception)[0:100]}")
            case MessageTypes.SUCCESS:
                prGreen(f"✅ {message}")

        if displayTraceback:
            traceback.print_exc()
