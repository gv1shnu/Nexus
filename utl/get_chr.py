"""Chrome Installation Checker"""

# Python standard library
import os

# Internal import
from utl.logger import Logger

SUPPORTED_PLATFORM = "Linux"
logger = Logger()


def is_chrome_installed() -> bool:
    """
    Check if Google Chrome is installed on the system.

    Returns:
        bool: True if Chrome is installed, False otherwise.
    """
    try:
        os_name = SUPPORTED_PLATFORM
        if os_name != SUPPORTED_PLATFORM:
            logger.critical(f"Incompatible OS found.")
            return False
        ans = os.system("dpkg -l | grep google-chrome-stable") == 0
        if not ans:
            logger.warning("Chrome is not installed on the system.")
        return ans
    except Exception as f:
        logger.error(f"An error occurred while checking Chrome installation: {f}")
        return False


if __name__ == '__main__':
    is_chrome_installed()
