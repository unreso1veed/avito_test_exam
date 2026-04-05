from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.driver_utils import get_driver
import time

#TC-D-06

STATS_LINK = (By.CSS_SELECTOR, "a[href='/stats']")
REFRESH_BTN = (By.CSS_SELECTOR, "button[class*='_refreshButton_']")
TIME_VALUE = (By.CSS_SELECTOR, "span[class*='_timeValue_']")

def get_time_seconds(time_str: str) -> int:
    parts = time_str.split(':')
    if len(parts) == 2:
        return int(parts[0]) * 60 + int(parts[1])
    return 0

def test_stats_update():
    driver = get_driver()
    try:
        driver.get("https://cerulean-praline-8e5aa6.netlify.app/")
        stats_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(STATS_LINK))
        stats_link.click()

        time_elem = WebDriverWait(driver, 10).until(EC.presence_of_element_located(TIME_VALUE))
        time.sleep(2)
        initial_seconds = get_time_seconds(time_elem.text)

        refresh_btn = driver.find_element(*REFRESH_BTN)
        refresh_btn.click()

        #ждем обновления таймера
        WebDriverWait(driver, 10).until(
            lambda d: get_time_seconds(d.find_element(*TIME_VALUE).text) > initial_seconds
        )
        new_seconds = get_time_seconds(driver.find_element(*TIME_VALUE).text)
        assert new_seconds > initial_seconds, f"Таймер не сбросился: {initial_seconds} -> {new_seconds} сек"
    finally:
        driver.quit()