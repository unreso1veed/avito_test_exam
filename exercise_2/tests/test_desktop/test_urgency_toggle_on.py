from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.driver_utils import get_driver

#TC-D-05

URGENT_LABEL = (By.XPATH, "//label[contains(., 'Только срочные')]")
ITEM_CARD = (By.CSS_SELECTOR, "div[class*='_card__content_']")
CARD_TITLE = (By.CSS_SELECTOR, "h3[class*='_card__title_']")
CARD_PRICE = (By.CSS_SELECTOR, "div[class*='_card__price_']")
URGENT_BADGE = (By.CSS_SELECTOR, "span[class*='_card__priority_']")
PRICE_ITEM = (By.CSS_SELECTOR, "[class*='_card__price_']")

def test_urgent_toggle():
    driver = get_driver()
    try:
        driver.get("https://cerulean-praline-8e5aa6.netlify.app/")
        
        #выключаем тогл через js
        #выключил так, потому что при дефолтном клике через селениум не сработало
        label = WebDriverWait(driver, 15).until(EC.presence_of_element_located(URGENT_LABEL))
        driver.execute_script("arguments[0].scrollIntoView(true);", label)
        checkbox = label.find_element(By.TAG_NAME, "input")
        if not checkbox.is_selected():
            driver.execute_script("arguments[0].click();", label)
        
        WebDriverWait(driver, 15).until(EC.presence_of_element_located(PRICE_ITEM))
        
        cards = driver.find_elements(*ITEM_CARD)
        assert len(cards) > 0, "После включения тогла нет объявлений"
        
        errors = []
        for idx, card in enumerate(cards, start=1):
            #получаем название и цену
            title = "неизвестно"
            price = "неизвестно"
            try:
                title_elem = card.find_element(*CARD_TITLE)
                title = title_elem.text.strip()
            except:
                pass
            try:
                price_elem = card.find_element(*CARD_PRICE)
                price = price_elem.text.strip()
            except:
                pass
            
            badges = card.find_elements(*URGENT_BADGE)
            if len(badges) != 1 or "Срочно" not in badges[0].text:
                errors.append(f"Карточка #{idx} (\"{title}\", {price}): плашек {len(badges)} (ожидаем 1 со статусом 'Срочно')")
        
        #если есть ошибки 
        if errors:
            error_msg = "Найдены объявления без статуса 'Срочно' при включённом тогле:\n" + "\n".join(errors)
            assert False, error_msg
        
        #выключаем тогл
        if checkbox.is_selected():
            driver.execute_script("arguments[0].click();", label)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(PRICE_ITEM))
        prices = driver.find_elements(*PRICE_ITEM)
        assert len(prices) > 0, "После выключения тогла нет объявлений"
        
    finally:
        driver.quit()