from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Initialize the browser (Chrome)
driver = webdriver.Chrome()
driver.get('https://www.google.com')

time.sleep(2)  # Wait for the page to load

# Find the search box, enter 'flipkart', and submit
search_box = driver.find_element(By.NAME, 'q')
search_box.send_keys('flipkart')
search_box.send_keys(Keys.RETURN)

time.sleep(2)  # Wait for search results

# Click the Flipkart website link (first result with 'flipkart.com')
links = driver.find_elements(By.XPATH, "//a[contains(@href, 'flipkart.com')]")
if links:
    links[0].click()
else:
    print('Flipkart link not found in search results.')

time.sleep(5)  # Let the user see the Flipkart page
driver.quit()
