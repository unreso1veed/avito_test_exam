from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from utils.driver_utils import get_driver

#TC-D-04

CATEGORY_SELECT = (By.XPATH, "(//select[contains(@class, '_filters__select_')])[3]")
PRICE_ITEM = (By.CSS_SELECTOR, "[class*='_card__price_']")
ITEM_CATEGORY = (By.CSS_SELECTOR, "[class*='_card__category_']")

def test_category_filter():
    driver = get_driver()
    try:
        driver.get("https://cerulean-praline-8e5aa6.netlify.app/")
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(CATEGORY_SELECT)
        )
        
        cat_select = Select(driver.find_element(*CATEGORY_SELECT))
        cat_select.select_by_visible_text("Электроника")
        
        #ждем появления цен
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(PRICE_ITEM)
        )
        
        #ждем появления категорий
        WebDriverWait(driver, 10).until(
            lambda d: any(el.text.strip() for el in d.find_elements(*ITEM_CATEGORY))
        )
        
        category_elements = driver.find_elements(*ITEM_CATEGORY)
        categories = [el.text.strip() for el in category_elements]
        
        for cat in categories:
            assert cat == "Электроника", f"Неверная категория: {cat}"
        
        assert len(categories) > 0, "Нет объявлений после фильтрации"
        
    finally:
        driver.quit()