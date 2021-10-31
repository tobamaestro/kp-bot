import os
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

load_dotenv()

STATE_MAP = {
    'KAO_NOVO': '//*[@id="data[condition]as-new"]',
    'KORISCENO': '//*[@id="data[condition]used"]'
}
CURRENCY_MAP = {
    "DIN": '//*[@id="currency_rsd"]',
    "EUR": '//*[@id="currency_eur"]'
}

driver = webdriver.Chrome()
driver.get('https://novi.kupujemprodajem.com/login')

# parse file from Drive:
# name
# category?
# state_choice
# price
# currency_choice
# text (separate file? cause of multiline issue, hard to say when it ends or same file but last item would be advert text)

# upload photos from Drive


def get_element(driver, search_by, val):
    return driver.find_element(search_by, val)


# refactor - add search_by?
def wait_and_get_element(driver, search_by, val):
    return WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((search_by, val))
    )


def login(driver):
    get_element(
        driver, By.XPATH, '//*[@id="email"]').send_keys(os.getenv("USERNAME"))
    get_element(driver, By.XPATH,
                '//*[@id="password"]').send_keys(os.getenv("PASS"))
    get_element(driver, By.XPATH, '//*[@id="submitButton"]').click()


def create_new_advert(driver):
    wait_and_get_element(
        driver, By.XPATH, '//*[@id="adTable"]/div[3]/div/a').click()


def new_advert_first(driver):
    advertNameInput = get_element(
        driver, By.XPATH, '//*[@id="data[group_suggest_text]"]')
    advertNameInput.send_keys("esa tecar gume 190/65 R15")

    suggestCategoryBtn = get_element(
        driver, By.XPATH, '//*[@id="group-suggestions-holder"]/div/div[1]/div[2]/div[1]/input')
    suggestCategoryBtn.click()

    categoryLabel = wait_and_get_element(
        driver, By.XPATH, '//*[@id="groupSuggestionHolderTemplate"]')
    categoryLabel.click()


def attach_photos(driver):
    print("TO DO")


def new_advert_second(driver):
    stateChoice = wait_and_get_element(
        driver, By.XPATH, STATE_MAP['KORISCENO'])
    stateChoice.click()

    priceInput = get_element(driver, By.XPATH, '//*[@id="price_number"]')
    priceInput.send_keys("23")

    currencyChoice = get_element(
        driver, By.XPATH, CURRENCY_MAP['DIN'])
    currencyChoice.click()

    # WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it(
    #     (By.XPATH, '//*[@id="data[description]_ifr"]')))
    # advertTextInput = WebDriverWait(driver, 20).until(
    #     EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[2]/div/div[1]/div/form/div[5]/div/div/div[2]/div[2]/div[16]/div[2]/div[1]/textarea')))
    # advertTextInput = get_element(
    # driver, By.XPATH, '//*[@id="tinymce"]')
    # advertTextInput.click()
    # advertTextInput.send_keys("neki moj oglascic")

    attach_photos(driver)


def new_advert_third(driver):
    standardVisibilityChoice = wait_and_get_element(
        driver, By.XPATH, '//*[@id="data[promo_type]none"]')  # data\[promo_type\]none
    standardVisibilityChoice.click()


def new_advert_final(driver):
    acceptTOSBox = wait_and_get_element(
        driver, By.XPATH, '//*[@id="accept_yes"]')  # accept_yes
    acceptTOSBox.click()


login(driver)
create_new_advert(driver)

new_advert_first(driver)

new_advert_second(driver)
time.sleep(5)
get_element(driver, By.XPATH,
            '//*[@id="adFormProgressHolderInner"]/div[5]/div[3]/div/input').click()  # next page

new_advert_third(driver)
get_element(driver, By.XPATH,
            '//*[@id="adFormProgressHolderInner"]/div[5]/div[4]/div/input').click()  # next page

new_advert_final(driver)

# submit advert
get_element(driver, By.XPATH,
            '//*[@id="adFormDeclaration"]/div[8]/div/input').click()

driver.quit()
