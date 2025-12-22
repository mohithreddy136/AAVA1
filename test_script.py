from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import time

# -------------------------------
# Headless Chrome for CI
# -------------------------------
options = Options()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1920,1080")

# Initialize the WebDriver with Headless Chrome options
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

try:
    # Navigate to Google website
    driver.get("https://www.google.com")

    # Wait for the page title to contain 'Google'
    WebDriverWait(driver, 10).until(EC.title_contains("Google"))

    # Print the page title
    print("Page Title:", driver.title)

    # Print the current URL
    print("Current URL:", driver.current_url)

    # Maximize the browser window
    # Note: In headless mode, maximize_window() may not have a visible effect,
    # but we include it for completeness.
    driver.maximize_window()
    print("Window maximized.")

    # Wait for 2 seconds to simulate user observation (optional)
    time.sleep(2)

    # Minimize the browser window
    # Note: In headless mode, minimize_window() may not have a visible effect,
    # but we include it for completeness.
    driver.minimize_window()
    print("Window minimized.")

    # Wait for 2 seconds to simulate user observation (optional)
    time.sleep(2)

except TimeoutException:
    print("An element was not found within the timeout period or the page did not load as expected.")

except Exception as e:
    print(f"An unexpected error occurred: {e}")

finally:
    # Close the browser
    driver.quit()
    print("Browser closed.")
