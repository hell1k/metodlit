import json
import os
import allure
import pytest
from selene import be
from selene.api import browser, s, ss

from selenium import webdriver

from pages.base_page import BasePage


def pytest_addoption(parser):
    parser.addoption('--base_url', action='store', default=os.getenv('base_url'), help='Base URL')


@pytest.fixture(scope="session")
def base_url(request):
    return request.config.getoption('--base_url')


def setup_browser(base_url):
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--headless")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-notifications")
    options.add_argument("--lang=en-US")
    options.add_argument("--log-level=1")
    # options.page_load_strategy = 'eager'
    browser.config.timeout = 10
    browser.config.base_url = base_url
    browser.config.driver_options = options
    BasePage().open_url(base_url)


@pytest.fixture()
def close_cookie():
    s("//button[contains(@class,'cookie-consent-popup__button')]").should(be.clickable).click()


@pytest.fixture()
def click_correct_city_btn():
    s("//button[contains(text(), 'Все верно')]").should(be.clickable).click()


def browser_teardown():
    BasePage.get_screenshot()
    console = browser.driver.get_log('browser')
    allure.attach(json.dumps(console), 'Console',
                  allure.attachment_type.JSON)
    browser.close()
    browser.quit()


@pytest.fixture()
def setup(request):
    base_url = request.config.getoption('--base_url')
    setup_browser(base_url)
    yield
    browser_teardown()
