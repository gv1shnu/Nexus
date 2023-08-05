from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import ChromeOptions
from src.chr import chrome_installed


def initialise_driver():
    if not chrome_installed:
        return

    try:
        service = Service(executable_path='./src/chromedriver.exe')
        options = ChromeOptions()
        options.add_argument("--headless --no-sandbox --disable-dev-shm-usage --disable-gpu")
        _driver = webdriver.Chrome(service=service, options=options)
        str1 = _driver.capabilities['browserVersion']
        str2 = _driver.capabilities['chrome']['chromedriverVersion'].split(' ')[0]
    except Exception as e:
        print(f"Exception at driver: {str(e)}")
        exit(12)

    x = int(str1.split('.')[0])
    y = int(str2.split('.')[0])
    if x != y:
        _driver.quit()
        print(f"Chrome browser version: {str1}")
        print(f"Chrome driver version: {str2}")
        raise ValueError("Please download the same chromedriver version")

    return _driver


driver = initialise_driver()
