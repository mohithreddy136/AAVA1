from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager

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

    # Step 2: Wait for the search box to be present
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "q"))
    )

    # Step 3: Type 'selenium' into the search box
    search_box.send_keys("selenium")

    # Step 4: Wait for the suggestions box to appear
    suggestions_box = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "ul[role='listbox']"))
    )

    # Step 5: Collect all suggestion elements
    suggestions = suggestions_box.find_elements(By.CSS_SELECTOR, "li span")

    # Step 6: Store all suggestion texts in a variable
    suggestion_texts = [s.text for s in suggestions if s.text.strip() != ""]

    # Step 7: Print the number of suggestions
    print(len(suggestion_texts))

except TimeoutException:
    print("An element was not found within the timeout period.")

finally:
    # Close the browser
    driver.quit()