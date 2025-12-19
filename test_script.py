import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException

def main():
    # Path to your chromedriver executable, update as needed
    CHROMEDRIVER_PATH = 'chromedriver'

    # Initialize Chrome WebDriver with options
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    # options.add_argument('--headless')  # Uncomment if you want to run in headless mode

    try:
        driver = webdriver.Chrome(service=ChromeService(CHROMEDRIVER_PATH), options=options)
        wait = WebDriverWait(driver, 10)

        # Step 1: Open Google
        driver.get('https://www.google.com')
        print("Opened Google homepage.")

        # Step 2: Search for 'Flipkart'
        search_box = wait.until(EC.presence_of_element_located((By.NAME, 'q')))
        search_box.clear()
        search_box.send_keys('Flipkart')
        search_box.send_keys(Keys.RETURN)
        print("Searched for 'Flipkart'.")

        # Step 3: Click on the Flipkart website link from search results
        try:
            flipkart_link = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'flipkart.com') and not(contains(@href, 'accounts.google.com'))]"))
            )
            flipkart_link.click()
            print("Clicked on Flipkart link in search results.")
        except TimeoutException:
            print("Flipkart link not found in search results.")
            return

        # Step 4: Wait for Flipkart homepage to load and perform assertions
        try:
            # Wait for the Flipkart logo to be present
            logo = wait.until(
                EC.presence_of_element_located((By.XPATH, "//img[contains(@title, 'Flipkart')]") )
            )
            print("Flipkart logo found on homepage.")

            # Assert the page title contains 'Flipkart'
            assert 'Flipkart' in driver.title, "Page title does not contain 'Flipkart'"
            print("Page title contains 'Flipkart'.")
        except (TimeoutException, AssertionError, NoSuchElementException) as e:
            print(f"Assertion failed: {e}")
        else:
            print("All assertions passed successfully.")

    except WebDriverException as e:
        print(f"WebDriver error: {e}")
    finally:
        # Step 5: Teardown - Close the browser
        driver.quit()
        print("Browser closed.")

if __name__ == '__main__':
    main()
