# driver service to be initialised at the start and shared without causing cyclic dependencies

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

driver_service = webdriver.chrome.service.Service(ChromeDriverManager().install())
