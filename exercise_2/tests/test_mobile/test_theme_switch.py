from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.driver_utils import get_mobile_driver

#TC-M-01

THEME_TOGGLE = (By.CSS_SELECTOR, "button[class*='_themeToggle_']")

def test_theme_switch():
    driver = get_mobile_driver()
    try:
        driver.get("https://cerulean-praline-8e5aa6.netlify.app/")
        toggle = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(THEME_TOGGLE))
        
        #запомнили текущую тему
        initial_label = toggle.get_attribute("aria-label")
        
        toggle.click()
        
        WebDriverWait(driver, 10).until(
            lambda d: d.find_element(*THEME_TOGGLE).get_attribute("aria-label") != initial_label
        )
       
        new_label = driver.find_element(*THEME_TOGGLE).get_attribute("aria-label")
        assert new_label != initial_label, "Тема не переключилась"
    finally:
        driver.quit()