from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def get_driver():
    service = Service(ChromeDriverManager().install())
    options = Options ()
    options.add_argument('--start-maximized')
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def get_mobile_driver(device_name = "iPhone 12 Pro"):
    service = Service(ChromeDriverManager().install())
    options = Options()
    options.add_experimental_option('mobileEmulation', {'deviceName': device_name})
    driver = webdriver.Chrome(service=service, options=options)
    return driver