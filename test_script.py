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
from selenium.common.exceptions import TimeoutException, NoSuchElementException
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

@pytest.fixture(scope="function")
def wait(driver):
    return WebDriverWait(driver, 10)

def accept_cookies_if_present(driver, wait):
    try:
        consent_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//button[.//div[text()="I agree"] or .//div[text()="Accept all"] or @id="L2AGLb"]'))
        )
        consent_button.click()
        take_screenshot(driver, "accepted_cookies")
    except TimeoutException:
        pass

@pytest.mark.usefixtures("driver", "wait")
def test_google_search_and_navigation(driver, wait):
    driver.get("https://www.google.com")
    take_screenshot(driver, "google_homepage")
    accept_cookies_if_present(driver, wait)

    search_box = wait.until(EC.presence_of_element_located((By.NAME, "q")))
    search_box.clear()
    search_box.send_keys("pen")
    search_box.send_keys(Keys.RETURN)
    take_screenshot(driver, "search_for_pen")

    results = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div#search .g")))
    assert results, "No search results found."
    take_screenshot(driver, "search_results")

    first_result = results[0]
    link = first_result.find_element(By.TAG_NAME, "a")
    link_href = link.get_attribute("href")
    assert link_href is not None, "First result link does not have href."
    link.click()
    take_screenshot(driver, "opened_first_result")

    wait.until(EC.url_changes("https://www.google.com"))
    current_url = driver.current_url
    assert current_url == link_href or link_href in current_url, "URL after clicking the link does not match expected."
    take_screenshot(driver, "assertion_url_check")

    page_title = driver.title
    assert page_title.strip() != "", "Page title is empty."
    take_screenshot(driver, "assertion_title_check")
