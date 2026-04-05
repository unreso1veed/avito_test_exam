import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.driver_utils import get_driver

#TC-D-08

STATS_LINK = (By.CSS_SELECTOR, "a[href='/stats']")
TOGGLE_BTN = (By.CSS_SELECTOR, "button[class*='_toggleButton_']")
DISABLED_TEXT = (By.CSS_SELECTOR, "div[class*='_disabled_']")

def test_stats_timer_start():
    driver = get_driver()
    try:
        driver.get("https://cerulean-praline-8e5aa6.netlify.app/")
        stats_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(STATS_LINK))
        stats_link.click()

        #стопаем таймер
        toggle_btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(TOGGLE_BTN))
        if not driver.find_elements(*DISABLED_TEXT):
            toggle_btn.click()
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located(DISABLED_TEXT))

        #запускаем таймер
        toggle_btn = driver.find_element(*TOGGLE_BTN)
        toggle_btn.click()

        time.sleep(3)
        if driver.find_elements(*DISABLED_TEXT):
            assert False, "Таймер не возобновлён"
    finally:
        driver.quit()