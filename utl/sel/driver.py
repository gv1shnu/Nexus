"""Selenium ChromeDriver Setup"""

# Python standard library
import os.path

# Third party libraries
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import ChromeOptions

# Internal imports
from decl import CDR_PATH, OS_NAME, CHROMEDRIVER_PATH
from utl.sel.get_chr import is_chrome_installed
from utl.sel.get_driver import get_chromedriver_url, download, unzip
from utl.logger import Logger

logger = Logger()


def make_chromedriver_executable(driver_path: str):
    """
    Make the chromedriver executable.

    Args:
        driver_path (str): Path to the chromedriver executable.
    """
    try:
        os.chmod(driver_path, 0o755)  # Set execute permission
        logger.info("Chromedriver made executable")
    except Exception as e:
        logger.error(f"Failed to make chromedriver executable: {str(e)}")


def initialise_driver() -> webdriver.Chrome or None:
    """
    Initialize the Selenium WebDriver.

    Returns:
        webdriver.Chrome: Initialized Chrome WebDriver instance.
    """
    chrome_installed: bool = is_chrome_installed()
    if not chrome_installed:
        logger.warning("Chrome is not installed, so some functions might not work properly.")
        return None

    if not os.path.exists(CDR_PATH):
        logger.debug("Fetching chromedriver")
        try:
            cdurl = get_chromedriver_url()
            downloadStatus = download(cdurl, CDR_PATH, "chromedriver.zip")
            if downloadStatus:
                if not unzip():
                    logger.error("Chromedriver unzip failed")
                    return None
            else:
                logger.error("Chromedriver download failed")
                return None
            logger.info("Chromedriver successfully downloaded.")
        except Exception as e:
            logger.error(f"An error occurred while downloading chromedriver: {e}")
            return None

    if OS_NAME == "Linux":
        make_chromedriver_executable(CHROMEDRIVER_PATH)
    headless = "--headless=chrome"
    gpu = ""
    try:
        service = Service(executable_path=CHROMEDRIVER_PATH)
        options = ChromeOptions()
        options.add_argument(f"{headless} --no-sandbox --disable-dev-shm-usage {gpu}")
        _driver = webdriver.Chrome(service=service, options=options)
        browserVersion = _driver.capabilities['browserVersion']
        chromedriverVersion = _driver.capabilities['chrome']['chromedriverVersion'].split(' ')[0]
        if int(browserVersion.split('.')[0]) != int(chromedriverVersion.split('.')[0]):
            logger.debug(f"Chrome browser version: {browserVersion}")
            logger.debug(f"Chrome driver version: {chromedriverVersion}")
            logger.error("Please download the same chromedriver version")
            return None
    except Exception as e:
        logger.error(f"An error occurred while installing chromedriver: {e}")
        return None

    return _driver
