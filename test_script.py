from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# -------------------------------
# CI-safe Chrome configuration
# -------------------------------
chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=chrome_options
)

try:
    # Step 1: Navigate to Google
    driver.get("https://www.google.com")
    print("Opened Google homepage.")

    # Step 2: Wait for the search box
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "q"))
    )

    # Step 3: Search for Flipkart
    search_box.send_keys("Flipkart")
    search_box.send_keys(Keys.RETURN)

    # Step 4: Click Flipkart link
    flipkart_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//h3[contains(text(),'Flipkart')]"))
    )
    flipkart_link.click()

    # Step 5: Switch tab if opened
    if len(driver.window_handles) > 1:
        driver.switch_to.window(driver.window_handles[-1])

    # Step 6: Assertion – title contains Flipkart
    WebDriverWait(driver, 10).until(EC.title_contains("Flipkart"))
    assert "Flipkart" in driver.title

    print("✅ Flipkart page loaded successfully")

except (TimeoutException, AssertionError, NoSuchElementException) as e:
    print("❌ Test failed:", e)
    raise

finally:
    driver.quit()
