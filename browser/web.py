from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
import os

def browser():
    driver_path = os.path.abspath('.\Driver\geckodriver.exe')
    options = Options()
    options.add_argument('--headless')  
    options.add_argument('--disable-gpu')

    service = Service(executable_path=driver_path)
    driver = webdriver.Firefox(service=service, options=options)
    return driver
