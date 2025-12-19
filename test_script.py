from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

# Initialize the WebDriver (ensure chromedriver is in your PATH)
driver = webdriver.Chrome()

try:
    # Step 1: Navigate to Google
    driver.get("https://www.google.com")
    driver.maximize_window()

    # Accept cookies if the consent form appears (for EU users)
    try:
        consent_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'I agree') or contains(., 'Accept all')]"))
        )
        consent_btn.click()
    except TimeoutException:
        pass  # Consent form did not appear

    # Step 2: Search for "Flipkart"
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "q"))
    )
    search_box.send_keys("Flipkart")
    search_box.send_keys(Keys.RETURN)

    # Step 3: Click on the Flipkart link in search results
    flipkart_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//h3[contains(text(),'Flipkart')]/ancestor::a"))
    )
    flipkart_link.click()

    # Step 4: Switch to the new tab if opened
    time.sleep(2)
    if len(driver.window_handles) > 1:
        driver.switch_to.window(driver.window_handles[1])

    # Step 5: Assert Flipkart homepage loaded
    # Wait for the Flipkart logo or title
    WebDriverWait(driver, 10).until(
        EC.title_contains("Flipkart")
    )
    print("Page title is:", driver.title)
    assert "Flipkart" in driver.title, "Flipkart homepage did not load!"

    # Optionally, check for the Flipkart logo
    try:
        logo = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//img[contains(@src, 'flipkart')]"))
        )
        print("Flipkart logo found. Homepage loaded successfully.")
    except TimeoutException:
        print("Flipkart logo not found, but title assertion passed.")

except (TimeoutException, NoSuchElementException) as e:
    print("Test failed:", str(e))

finally:
    # Close the browser
    driver.quit()
