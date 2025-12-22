from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

def setup_driver():
    # Set up Headless Chrome for CI
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    return driver

def select_menu_actions(driver):
    wait = WebDriverWait(driver, 10)
    driver.get("https://demoqa.com/select-menu")

    # Select "Group 2, option 1" from "Select Value"
    try:
        select_value = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@id='withOptGroup']//div[contains(@class,'css-1hwfws3')]")))
        select_value.click()
        option = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[text()='Group 2, option 1']")))
        option.click()
        print("Selected 'Group 2, option 1' in Select Value dropdown.")
    except Exception as e:
        print(f"Error selecting 'Group 2, option 1': {e}")

    # Select "Mr." from "Select One"
    try:
        select_one = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@id='selectOne']//div[contains(@class,'css-1hwfws3')]")))
        select_one.click()
        mr_option = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[text()='Mr.']")))
        mr_option.click()
        print("Selected 'Mr.' in Select One dropdown.")
    except Exception as e:
        print(f"Error selecting 'Mr.': {e}")

    # Select "Green" from Old Style Select Menu
    try:
        old_style_select = Select(driver.find_element(By.ID, "oldSelectMenu"))
        old_style_select.select_by_visible_text("Green")
        print("Selected 'Green' in Old Style Select Menu.")
    except Exception as e:
        print(f"Error selecting from old style menu: {e}")

    # Select "Blue" and "Black" from Multi Select DropDown
    try:
        multi_select = driver.find_element(By.XPATH, "//div[@class=' css-2b097c-container']")
        multi_select.click()
        blue_option = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[text()='Blue']")))
        blue_option.click()
        black_option = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[text()='Black']")))
        black_option.click()
        # Click outside to close dropdown
        driver.find_element(By.TAG_NAME, "body").click()
        print("Selected 'Blue' and 'Black' in Multi Select DropDown.")
    except Exception as e:
        print(f"Error in multi select: {e}")

def checkbox_actions(driver):
    wait = WebDriverWait(driver, 10)
    driver.get("https://demoqa.com/checkbox")

    # Expand all checkboxes
    try:
        expand_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".rct-option-expand-all")))
        expand_button.click()
        print("Expanded all checkboxes.")
    except Exception as e:
        print(f"Error expanding all checkboxes: {e}")

    # Check 'Home' parent checkbox
    try:
        home_checkbox = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".rct-checkbox")))
        home_checkbox.click()
        # Validate
        checked = driver.find_element(By.CSS_SELECTOR, ".rct-icon-check")
        assert checked.is_displayed(), "Home checkbox not checked"
        print("Checked 'Home' checkbox.")
    except Exception as e:
        print(f"Error checking 'Home' checkbox: {e}")

    # Optionally, check 'Documents' and 'Downloads'
    try:
        documents_checkbox = driver.find_element(By.XPATH, "//span[text()='Documents']/preceding-sibling::span[@class='rct-checkbox']")
        documents_checkbox.click()
        print("Checked 'Documents' checkbox.")
        downloads_checkbox = driver.find_element(By.XPATH, "//span[text()='Downloads']/preceding-sibling::span[@class='rct-checkbox']")
        downloads_checkbox.click()
        print("Checked 'Downloads' checkbox.")
    except NoSuchElementException:
        print("Documents or Downloads checkbox not found.")
    except Exception as e:
        print(f"Error checking 'Documents' or 'Downloads': {e}")

def main():
    driver = setup_driver()
    try:
        select_menu_actions(driver)
        checkbox_actions(driver)
        print("Automation steps completed successfully.")
    except Exception as e:
        print(f"Test failed: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
