from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from utils.driver_utils import get_driver

#TC-D-02

SORT_FIELD_SELECT = (By.XPATH, "(//select[contains(@class, '_filters__select_')])[1]")
SORT_DIRECTION_SELECT = (By.XPATH, "(//select[contains(@class, '_filters__select_')])[2]")
PRICE_ITEM = (By.CSS_SELECTOR, "[class*='_card__price_']")

def test_price_sort_asc():
    driver = get_driver()
    try:
        driver.get("https://cerulean-praline-8e5aa6.netlify.app/")
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(SORT_FIELD_SELECT)
        )
        
        #выбираем по цене
        field_select = Select(driver.find_element(*SORT_FIELD_SELECT))
        field_select.select_by_visible_text("Цене")
        
        #выбираем по возрастанию
        dir_select = Select(driver.find_element(*SORT_DIRECTION_SELECT))
        dir_select.select_by_visible_text("По возрастанию")
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(PRICE_ITEM)
        )
        
        #собираем все цены
        price_elements = driver.find_elements(*PRICE_ITEM)
        prices = []
        for el in price_elements:
            text = el.text.replace("₽", "").replace(" ", "").replace(",", "").strip()
            if text.isdigit():
                prices.append(int(text))
        
        #проверка возрастания цен
        for i in range(len(prices) - 1):
            assert prices[i] <= prices[i+1], f"Цены не по возрастанию: {prices[i]} > {prices[i+1]}"
        
        assert len(prices) > 0, "Нет объявлений после сортировки"
        
    finally:
        driver.quit()