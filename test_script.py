from selenium import webdriver
from selenium.webdriver.common.by import By
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
    # Step 1: Open Flipkart directly
    driver.get("https://www.flipkart.com")

    # Step 2: Assert title
    WebDriverWait(driver, 15).until(EC.title_contains("Flipkart"))
    assert "Flipkart" in driver.title

    print("✅ Flipkart homepage loaded successfully")

except TimeoutException as e:
    print("❌ Timeout waiting for Flipkart page:", e)
    raise

finally:
    driver.quit()
