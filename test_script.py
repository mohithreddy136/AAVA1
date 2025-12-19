from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Initialize the WebDriver (ensure chromedriver is in your PATH)
driver = webdriver.Chrome()

try:
    # Step 1: Navigate to Google
    driver.get("https://www.google.com")
    print("Opened Google homepage.")

    # Step 2: Wait for the search box to be present
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "q"))
    )
    print("Google search box found.")

    # Step 3: Search for 'Flipkart'
    search_box.clear()
    search_box.send_keys("Flipkart")
    search_box.send_keys(Keys.RETURN)
    print("Searched for Flipkart.")

    # Step 4: Wait for search results to load and click the Flipkart link
    flipkart_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a/h3[contains(text(),'Flipkart')]"))
    )
    flipkart_link.click()
    print("Clicked on the Flipkart link in search results.")

    # Step 5: Switch to the new window/tab if opened
    driver.switch_to.window(driver.window_handles[-1])

    # Step 6: Wait for Flipkart homepage to load by checking for a key element
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "img[title='Flipkart']"))
    )
    print("Flipkart homepage loaded.")

    # Step 7: Basic Assertions
    # Assertion 1: Check if the page title contains 'Flipkart'
    assert "Flipkart" in driver.title, "Page title does not contain 'Flipkart'"
    print("Assertion passed: Page title contains 'Flipkart'.")

    # Assertion 2: Check if the Flipkart logo is present
    try:
        logo = driver.find_element(By.CSS_SELECTOR, "img[title='Flipkart']")
        assert logo.is_displayed(), "Flipkart logo is not displayed."
        print("Assertion passed: Flipkart logo is displayed.")
    except NoSuchElementException:
        print("Flipkart logo not found on the page.")

except TimeoutException as e:
    print(f"TimeoutException: {str(e)}")
except AssertionError as e:
    print(f"AssertionError: {str(e)}")
finally:
    # Close the browser
    driver.quit()
    print("Browser closed.")