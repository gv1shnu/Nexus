from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

driver_service = webdriver.chrome.service.Service(ChromeDriverManager().install())
