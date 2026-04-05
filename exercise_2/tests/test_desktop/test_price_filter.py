from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.driver_utils import get_driver

#TC-D-01

MIN_PRICE_INPUT = (By.CSS_SELECTOR, "input[placeholder='От']")
MAX_PRICE_INPUT = (By.CSS_SELECTOR, "input[placeholder='До']")
PRICE_ITEM = (By.CSS_SELECTOR, "[class*='_card__price_']")  

def test_price_filter():
    driver = get_driver()
    try:
        driver.get("https://cerulean-praline-8e5aa6.netlify.app")
        
        #ждем загрузки полей ввода
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(MIN_PRICE_INPUT)
        )
        
        #вводим минимальную и максимальную цену
        min_input = driver.find_element(*MIN_PRICE_INPUT)
        max_input = driver.find_element(*MAX_PRICE_INPUT)
        min_input.clear()
        min_input.send_keys("1000")
        max_input.clear()
        max_input.send_keys("30000")
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(PRICE_ITEM)
        )
        
        price_elements = driver.find_elements(*PRICE_ITEM)
        prices = []
        for el in price_elements:
            text = el.text.replace("₽", "").replace(" ", "").replace(",", "").strip()
            if text.isdigit():
                prices.append(int(text))
        
        for price in prices:
            assert 1000 <= price <= 30000, f"Цена {price} вне диапазона"
        
        assert len(prices) > 0, "Нет объявлений после фильтрации"
        
    finally:
        driver.quit()