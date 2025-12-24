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

# Function to take screenshots after each step
def take_screenshot(driver, action_name):
    os.makedirs("screenshots", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"screenshots/{action_name}_{timestamp}.png"
    driver.save_screenshot(filename)
    print(f"Screenshot saved: {filename}")

# -------------------------------
# Headless Chrome for CI
# -------------------------------
options = Options()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

wait = WebDriverWait(driver, 10)

try:
    # Step 1: Open Google
    driver.get("https://www.google.com")
    take_screenshot(driver, "open_google")

    # Step 2: Locate the search box and type 'pen'
    search_box = wait.until(EC.presence_of_element_located((By.NAME, "q")))
    search_box.clear()
    search_box.send_keys("pen")
    take_screenshot(driver, "typed_pen")

    # Step 3: Wait for suggestions to appear and count them
    suggestions_box = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "ul[role='listbox']")))
    suggestions = suggestions_box.find_elements(By.CSS_SELECTOR, "li span")
    print(f"Number of suggestions: {len(suggestions)}")
    take_screenshot(driver, "suggestions_list")

    # Step 4: Press Enter to search for 'pen'
    search_box.send_keys(Keys.RETURN)
    wait.until(EC.title_contains("pen"))
    take_screenshot(driver, "search_results")

    # Step 5: Wait for search results and open the second link
    results = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div#search a")))
    # Filter out any links that are not visible or are advertisements
    valid_results = [a for a in results if a.is_displayed() and a.get_attribute("href")]
    if len(valid_results) < 2:
        raise Exception("Less than 2 search results found.")
    second_link = valid_results[1]
    second_link_url = second_link.get_attribute("href")
    second_link.click()
    take_screenshot(driver, "open_second_link")

    # Step 6: Switch to new tab if opened, else stay on the same page
    if len(driver.window_handles) > 1:
        driver.switch_to.window(driver.window_handles[1])

    # Step 7: Print the page title and URL
    wait.until(lambda d: d.title != "")
    print(f"Page Title: {driver.title}")
    print(f"Page URL: {driver.current_url}")
    take_screenshot(driver, "second_link_page")

except TimeoutException as e:
    print(f"Timeout occurred: {e}")
except Exception as ex:
    print(f"An error occurred: {ex}")
finally:
    driver.quit()
