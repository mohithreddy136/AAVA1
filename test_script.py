from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

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

        # Accept cookies if the consent form appears (for EU/UK users)
        try:
            consent_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[.//div[text()='I agree'] or .//div[text()='Accept all']]"))
            )
            consent_button.click()
        except TimeoutException:
            # Consent form did not appear
            pass

        # Step 2: Wait for the search box and type "selenium"
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "q"))
        )
        search_box.send_keys("selenium")

        # Step 3: Wait for suggestions to appear and count them
        suggestions_box = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "ul[role='listbox']"))
        )
        driver.save_screenshot("screenshots/hello.png")
        suggestions = suggestions_box.find_elements(By.CSS_SELECTOR, "li span")
        print(f"Number of search suggestions: {len(suggestions)}")

        # Step 4: Click the first suggestion
        if suggestions:
            suggestions[0].click()
        else:
            print("No suggestions found.")
            return

        # Step 5: Wait for the new page to load and print the title and URL
        WebDriverWait(driver, 10).until(
            EC.title_contains("selenium")
        )
        print(f"Page Title: {driver.title}")
        print(f"Page URL: {driver.current_url}")

    except TimeoutException as e:
        print(f"An element was not found within the timeout period: {e}")

    finally:
        # Close the browser
        driver.quit()

if __name__ == "__main__":
    main()
