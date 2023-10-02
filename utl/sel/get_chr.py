"""Chrome Installation Checker"""

# Python standard library
import os

# Internal imports
from decl import SUPPORTED_PLATFORMS, OS_NAME, MODE
from utl.logger import Logger

logger = Logger()


def is_chrome_installed() -> bool:
    """
    Check if Google Chrome is installed on the system.

    Returns:
        bool: True if Chrome is installed, False otherwise.
    """
    try:
        ans = None
        if MODE == "PRODUCTION" and OS_NAME == "Linux":
            ans = os.system("dpkg -l | grep google-chrome-stable") == 0
        elif MODE == "DEBUG" and OS_NAME == "Windows":
            ans = os.path.exists("C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe")
        if not ans:
            logger.warning("Chrome is not installed on the system.")
        return ans
    except Exception as f:
        logger.error(f"An error occurred while checking Chrome installation: {f}")
        return False


if __name__ == '__main__':
    is_chrome_installed()
