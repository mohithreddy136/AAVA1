from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os
from datetime import datetime


def take_screenshot(driver, action_name):
    os.makedirs("screenshots", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"screenshots/{action_name}_{timestamp}.png"
    driver.save_screenshot(filename)
    print(f"Screenshot saved: {filename}")


def main():
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

    try:
        # Step 1: Navigate to Google
        driver.get("https://www.google.com")
        take_screenshot(driver, "01_google_home")

        # Accept cookies if the consent form appears
        try:
            consent_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((
                    By.XPATH,
                    "//button[.//div[text()='I agree'] or .//div[text()='Accept all']]"
                ))
            )
            consent_button.click()
            take_screenshot(driver, "02_cookie_accepted")
        except TimeoutException:
            take_screenshot(driver, "02_cookie_not_shown")

        # Step 2: Search for "selenium"
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "q"))
        )
        search_box.send_keys("selenium")
        take_screenshot(driver, "03_search_typed")

        # Step 3: Suggestions
        suggestions_box = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "ul[role='listbox']"))
        )
        suggestions = suggestions_box.find_elements(By.CSS_SELECTOR, "li span")
        print(f"Number of search suggestions: {len(suggestions)}")
        take_screenshot(driver, "04_suggestions_visible")

        # Step 4: Click first suggestion
        if suggestions:
            suggestions[0].click()
            take_screenshot(driver, "05_first_suggestion_clicked")
        else:
            print("No suggestions found.")
            take_screenshot(driver, "05_no_suggestions")
            return

        # Step 5: Results page loaded
        WebDriverWait(driver, 10).until(
            EC.title_contains("selenium")
        )
        take_screenshot(driver, "06_results_page")
        print(f"Page Title: {driver.title}")
        print(f"Page URL: {driver.current_url}")

    except TimeoutException as e:
        take_screenshot(driver, "error_timeout")
        print(f"An element was not found within the timeout period: {e}")

    finally:
        driver.quit()


if __name__ == "__main__":
    main()

