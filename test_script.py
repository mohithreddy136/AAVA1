import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture(scope="function")
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    yield driver
    driver.quit()


def attach_screenshot(driver, name="Screenshot"):
    allure.attach(
        driver.get_screenshot_as_png(),
        name=name,
        attachment_type=allure.attachment_type.PNG
    )


@allure.feature("Basic Demo Tests")
@allure.story("Google page checks")
def test_google_title_pass(driver):
    driver.get("https://www.google.com")

    attach_screenshot(driver, "Google Home Page")

    assert "Google" in driver.title


@allure.feature("Basic Demo Tests")
@allure.story("Intentional failure")
def test_google_title_fail(driver):
    driver.get("https://www.google.com")

    attach_screenshot(driver, "Before Assertion Failure")

    # ❌ Intentional failure
    assert "Bing" in driver.title
