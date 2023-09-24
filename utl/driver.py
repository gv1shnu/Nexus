"""Selenium ChromeDriver Setup"""

# Python standard library
import os.path

# Third party libraries
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import ChromeOptions

# Internal imports
from utl.get_chr import is_chrome_installed
from utl.get_driver import get_chromedriver_url, download, unzip
from utl.logger import Logger

CDR_PATH = "./cdr"
logger = Logger()


def make_chromedriver_executable(driver_path: str):
    """
    Make the chromedriver executable.

    Args:
        driver_path (str): Path to the chromedriver executable.
    """
    try:
        logger.debug("Changing permission to make chromedriver executable")
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
            result: str = "linux64"
            cdurl = get_chromedriver_url()
            downloadStatus = download(cdurl, CDR_PATH, "chromedriver.zip")
            if downloadStatus:
                unzipStatus = unzip(f"{CDR_PATH}/chromedriver.zip", CDR_PATH, result)
                if not unzipStatus:
                    logger.error("Chromedriver unzip failed")
                    return None
            else:
                logger.error("Chromedriver download failed")
                return None
            logger.info("Chromedriver successfully downloaded.")
        except Exception as e:
            logger.error(f"An error occurred while downloading chromedriver: {e}")
            return None

    chrome_driver_path = f"{CDR_PATH}/chromedriver"
    make_chromedriver_executable(chrome_driver_path)
    headless = "--headless=chrome"
    gpu = ""
    try:
        service = Service(executable_path=chrome_driver_path)
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
