import os
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
    print(f"Screenshot saved: {filename}")

options = Options()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

try:
    driver.get("https://www.google.com")
    take_screenshot(driver, "open_google")
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "q"))
    )
    search_box.clear()
    search_box.send_keys("selenium")
    take_screenshot(driver, "enter_search_term")
    suggestions_box = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "ul[role='listbox']"))
    )
    take_screenshot(driver, "suggestions_visible")
    first_suggestion = suggestions_box.find_elements(By.TAG_NAME, "li")[0]
    first_suggestion.click()
    take_screenshot(driver, "clicked_first_suggestion")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "search"))
    )
    take_screenshot(driver, "search_results_loaded")
    print("Test completed successfully.")
except TimeoutException as e:
    print(f"An element was not found within the timeout period: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
finally:
    driver.quit()
