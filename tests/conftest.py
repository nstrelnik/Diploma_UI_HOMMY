import pytest
from selenium import webdriver
from selene import browser
from utils import attach
from dotenv import load_dotenv
from selenium.webdriver.chrome.options import Options
import tempfile
import os


@pytest.fixture(scope="session", autouse=True)
def load_env():
    load_dotenv()


@pytest.fixture(scope="function", autouse=True)
def browser_management():
    browser.config.base_url = "https://myhommy.ru"
    browser.config.window_width = 1920
    browser.config.window_height = 1080
    #
    # options = Options()
    # # options.add_argument('--headless=new')
    # browser.config.driver_options = options

    options = Options()
    # options.add_argument('--headless=new')
    selenoid_capabilities = {
        "browserName": "chrome",
        "browserVersion": "128.0",
        "selenoid:options": {
            "enableVNC": True,
            "enableVideo": True
        }
    }

    selenoid_login = os.getenv("SELENOID_LOGIN")
    selenoid_pass = os.getenv("SELENOID_PASS")
    selenoid_url = os.getenv("SELENOID_URL")

    options.capabilities.update(selenoid_capabilities)
    driver = webdriver.Remote(
        # command_executor=f"https://{selenoid_login}:{selenoid_pass}@{selenoid_url}/wd/hub",
        command_executor=f"https://user1:1234@selenoid.autotests.cloud/wd/hub",
        options=options)

    browser.config.driver = driver
    yield

    attach.add_screenshot(browser)
    attach.add_logs(browser)
    attach.add_html(browser)
    attach.add_video(browser)

    browser.quit()
