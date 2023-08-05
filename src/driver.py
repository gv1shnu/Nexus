from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import ChromeOptions
from src.chr import chrome_installed, os_name


def initialise_driver():
    if not chrome_installed:
        return

    if os_name == "Linux":
        chrome_driver_path = "./cdr/chromedriver"
        headless = "--headless=chrome"
        gpu = ""
    else:
        chrome_driver_path = "./cdr/chromedriver.exe"
        headless = "--headless"
        gpu = "--disable-gpu"
    try:
        service = Service(executable_path=chrome_driver_path)
        options = ChromeOptions()
        options.add_argument(f"{headless} --no-sandbox --disable-dev-shm-usage {gpu}")
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

