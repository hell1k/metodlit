import ast
import random
import re
import time
from datetime import date, timedelta
import os
import random
import allure
import pytest
from selene import query, be, command
from selene.api import s, ss

from selene.support.conditions.be import visible, hidden
from selene.support.shared import browser
from selenium.common import WebDriverException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class BasePage:
    @allure.step("Переход на страницу '{url}'")
    def open_url(self, url):
        browser.open(url)

    @allure.step("Переход на главную страницу")
    def open_base_url(self):
        browser.open(os.getenv('base_url'))

    def get_element_text(self, element, allureText=None):
        if allureText is not None:
            with allure.step(f"Получение текста из элемента '{allureText}'"):
                return element.get(query.text)
        else:
            return element.get(query.text)

    @allure.step("Взять тело из элемента '{allureText}'")
    def get_element_value(self, element, allureText):
        return element.get(query.tag)

    def set_text(self, element, text, fieldName=None):
        if fieldName is not None:
            with allure.step(f"Заполнение поля '{fieldName}' текстом '{text}'"):
                element.set_value(text)
        else:
            element.set_value(text)

    def click(self, element, text=None):
        if text is not None:
            with allure.step(f"Клик по элементу '{text}'"):
                self.wait_element(element)
                element.click()
        else:
            self.wait_element(element)
            element.click()

    # @allure.step("Получение атрибута")
    def get_attribute(self, element, attribute):
        return element.get(query.attribute(attribute))

    # @allure.step("Получение текущего url")
    def get_url(self):
        return browser.driver.current_url

    # @allure.step("Перемещение к элементу")
    def move_to(self, element):
        driver = browser.driver
        action = ActionChains(driver)
        action.move_to_element(element).perform()

    def move_to_element(self, element):
        element.perform(command.js.scroll_into_view)
        self.wait_a_second()

    def get_element(self, locator):
        driver = browser.driver
        return driver.find_element(By.XPATH, locator)

    def get_elements(self, locator):
        driver = browser.driver
        return driver.find_elements(By.XPATH, locator)

    def get_elements_amount(self, element):
        return len(element)

    def wait_a_second(self):
        time.sleep(1)

    def wait_a_moment(self):
        time.sleep(0.5)

    def wait(self, seconds):
        time.sleep(seconds)

    def wait_element(self, locator, text=None):
        if text is not None:
            with allure.step(f"Проверка наличия элемента '{text}'"):
                locator.should(be.visible)
        else:
            locator.should(be.visible)

    def checking_presence_of_element(self, locator, text=None):
        if text is not None:
            with allure.step(f"Проверка наличия элемента '{text}'"):
                locator.should(be.present)
        else:
            locator.should(be.present)

    def wait_element_hidden(self, element, text=None):
        if text is not None:
            with allure.step(f"Проверка отсутствия элемента '{text}'"):
                element.should(be.hidden)
        else:
            element.should(be.hidden)

    @allure.step("Сравнение значений {expression1} и {expression2}")
    def assert_check_expressions(self, expression1, expression2, error_text=None):
        assert expression1 == expression2, error_text

    @allure.step("Сравнение значений {value1} и {value2}")
    def assert_values_equality(self, value1, value2, error_text=None):
        assert value1 == value2, error_text

    @allure.step("Проверка не соответсвия значений {expression1} и {expression2}")
    def assert_check_not_expressions(self, expression1, expression2, error_text=None):
        assert expression1 != expression2, error_text

    @allure.step("Проверка наличия текста {expression1} в {expression2}")
    def assert_check_coincidence(self, expression1, expression2, error_text):
        assert expression1 in expression2, error_text

    @allure.step("Проверка наличия текста {value1} в {value2}")
    def assert_text_availability(self, value1, value2, error_text):
        assert value1 in value2, error_text

    @allure.step("Проверка числового значения в пределах {value_from} в {value_to}")
    def assert_check_range(self, value_from, value_to, value_check, error_text):
        assert value_from <= value_check <= value_to, error_text

    @allure.step("Сравнение значений {expression1} больше {expression2}")
    def assert_check_comparison(self, expression1, expression2, error_text):
        assert expression1 > expression2, error_text

    @allure.step("Клик Enter в поле '{fieldName}'")
    def push_enter(self, element, fieldName=None):
        element.send_keys(Keys.ENTER)

    @allure.step("Клик Backspace в поле '{fieldName}'")
    def push_backspace(self, element, fieldName=None):
        element.send_keys(Keys.BACKSPACE)

    # @allure.step("Очистить поле '{fieldName}'")
    def field_clear(self, element, fieldName=None):
        if fieldName is not None:
            with allure.step(f"Очистка поля '{fieldName}'"):
                element.send_keys(Keys.LEFT_CONTROL + 'a')
                element.send_keys(Keys.DELETE)
        else:
            element.send_keys(Keys.LEFT_CONTROL + 'a')
            element.send_keys(Keys.DELETE)
        self.wait_a_moment()

    @allure.step("Назад в браузере")
    def browser_back(self):
        self.execute_script("window.history.go(-1)")
        # browser.driver.back()
        self.wait_a_second()

    @staticmethod
    def get_screenshot():
        allure.attach(
            name="Скриншот",
            body=browser.driver.get_screenshot_as_png(),
            attachment_type=allure.attachment_type.PNG,
        )

    @staticmethod
    def get_title():
        return browser.driver.title

    @staticmethod
    def get_random_element(elements_list):
        return elements_list[random.randrange(0, len(elements_list))]

    # @allure.step("Получение числа из строки")
    def get_number_from_element(self, element):
        return int(re.sub('[^0-9]', "", self.get_element_text(element)))

    def get_number_from_string(self, string):
        return int(re.sub('[^0-9]', "", string))


    # @allure.step("get_field_value js")
    def execute_script(self, script):
        return browser.driver.execute_script(script)

    # @allure.step("Получение тега элемента")
    def get_element_tag(self, element):
        return element.get(query.tag)

    @allure.step("Обновление страницы")
    def reload_page(self):
        browser.driver.refresh()

    def click_page_down(self):
        self.get_element('//body').send_keys(Keys.PAGE_DOWN)

    def click_page_up(self):
        self.get_element('//body').send_keys(Keys.PAGE_UP)

    def get_date_before_current(self, number):
        date_before_current = date.today() - timedelta(days=number)
        return date_before_current.strftime('%Y-%m-%d')

    @allure.step("Клик по кнопке '{button_text}'")
    def click_button(self, button_text):
        self.click(s(f"//button[contains(text(), '{button_text}')]"), f'кнопка {button_text}')
        self.wait_a_second()

    @allure.step("Проверка наличия заголовка '{title}'")
    def checking_title(self, title):
        self.wait_element(s(f"//h1[contains(text(), '{title}')]"))

    @allure.step("Проверка наличия на странице элемента с текстом '{text}'")
    def checking_text(self, text):
        self.wait_element(s(f"//*[contains(text(), '{text}')]"))

    def get_element_screenshot(self, element, file_name):
        self.get_element(element).screenshot(file_name)
