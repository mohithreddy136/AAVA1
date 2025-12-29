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

@pytest.fixture(scope="function")
def driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    yield driver
    driver.quit()

@pytest.fixture(scope="function")
def wait(driver):
    return WebDriverWait(driver, 10)

def accept_google_consent_if_present(driver, wait):
    try:
        consent_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'I agree') or contains(., 'Accept all')]")
        )
        consent_button.click()
        take_screenshot(driver, "accept_cookies")
        return True
    except TimeoutException:
        return False

def test_open_google(driver, wait):
    driver.get("https://www.google.com")
    take_screenshot(driver, "open_google")
    assert "Google" in driver.title
    accepted = accept_google_consent_if_present(driver, wait)
    # Accepting cookies is optional, so no assertion here

def test_open_facebook(driver, wait):
    driver.get("https://www.facebook.com")
    take_screenshot(driver, "open_facebook")
    assert "Facebook" in driver.title or "Facebook" in driver.page_source

def test_back_to_google(driver, wait):
    driver.get("https://www.google.com")
    accept_google_consent_if_present(driver, wait)
    driver.get("https://www.facebook.com")
    take_screenshot(driver, "open_facebook")
    driver.back()
    wait.until(EC.presence_of_element_located((By.NAME, "q")))
    take_screenshot(driver, "back_to_google")
    assert "Google" in driver.title

def test_search_pen_on_google(driver, wait):
    driver.get("https://www.google.com")
    accept_google_consent_if_present(driver, wait)
    search_box = wait.until(EC.presence_of_element_located((By.NAME, "q")))
    search_box.clear()
    search_box.send_keys("pen")
    search_box.send_keys(Keys.RETURN)
    wait.until(EC.presence_of_element_located((By.ID, "search")))
    take_screenshot(driver, "search_pen")
    assert "pen" in driver.title.lower() or "pen" in driver.page_source
