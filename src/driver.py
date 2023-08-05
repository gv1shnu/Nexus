# driver service to be initialised at the start and shared without causing cyclic dependencies
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


service = Service()
options = Options()
options.add_argument("--headless --no-sandbox --disable-dev-shm-usage --disable-gpu")
driver_service = webdriver.Chrome(service=service, options=options)
