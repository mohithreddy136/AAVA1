import os
import pytest
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager

def take_screenshot(driver, action_name):
    os.makedirs("screenshots", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"screenshots/{action_name}_{timestamp}.png"
    driver.save_screenshot(filename)

@pytest.fixture(scope="session")
def chrome_options():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    return options

@pytest.fixture(scope="function")
def driver(chrome_options):
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )
    yield driver
    driver.quit()

@pytest.mark.usefixtures("driver")
def test_google_search_flow(driver):
    driver.get("https://www.google.com")
    take_screenshot(driver, "open_google")
    assert "Google" in driver.title

    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "q"))
    )
    assert search_box.is_displayed()
    search_box.send_keys("selenium")
    take_screenshot(driver, "enter_search_term")
    search_box.send_keys(Keys.RETURN)

    try:
        suggestions_box = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "ul[role='listbox'] li"))
        )
        first_suggestion = driver.find_element(By.CSS_SELECTOR, "ul[role='listbox'] li")
        assert first_suggestion.is_displayed()
        first_suggestion.click()
        take_screenshot(driver, "click_first_suggestion")
    except TimeoutException:
        first_result = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "h3"))
        )
        assert first_result.is_displayed()
        first_result.click()
        take_screenshot(driver, "click_first_result")

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )
    take_screenshot(driver, "final_page")
    assert driver.current_url != "https://www.google.com/"
