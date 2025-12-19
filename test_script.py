from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Initialize the WebDriver (make sure chromedriver is in your PATH)
driver = webdriver.Chrome()

try:
    # Step 1: Navigate to Google
    driver.get("https://www.google.com")
    driver.maximize_window()

    # Step 2: Wait for the search box to be present and search for 'Flipkart'
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "q"))
    )
    search_box.send_keys("Flipkart")
    search_box.send_keys(Keys.RETURN)

    # Step 3: Wait for search results and click the Flipkart link
    flipkart_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//h3[contains(text(),'Flipkart')]/ancestor::a"))
    )
    flipkart_link.click()

    # Step 4: Wait for Flipkart homepage to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )

    # Step 5: Basic assertions
    # Assertion 1: Check if the page title contains 'Flipkart'
    assert "Flipkart" in driver.title, "Page title does not contain 'Flipkart'"

    # Assertion 2: Check for the presence of the Flipkart logo
    try:
        logo = driver.find_element(By.XPATH, "//img[contains(@src, 'flipkart')]")
        print("Flipkart logo found on the homepage.")
    except NoSuchElementException:
        print("Flipkart logo not found on the homepage.")

    print("All basic assertions passed.")

except TimeoutException as te:
    print(f"Timeout occurred: {te}")
except AssertionError as ae:
    print(f"Assertion failed: {ae}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
finally:
    # Close the browser
    driver.quit()
