import os

import allure
from selene.api import s, ss

from pages.base_page import BasePage
from pages.common.header import Header


class AuthorizationPage(BasePage):
    def __init__(self):
        self.header = Header()

    login_tab = s("//a[@href='login']")
    phone = s("//input[@inputmode='tel']")
    email_btn = s("//a[contains(text(), 'Войти с помощью E-mail')]")
    email_field = s("//input[@placeholder='Введите e-mail']")
    password_field = s("//input[@placeholder='Введите пароль']")
    login_btn = s("//button[contains(text(), 'Войти')]")
    incorrect_login_or_password_message = s("//div[text()='Неправильный логин или пароль']")

    @allure.step("Клик Авторизация")
    def click_authorization(self):
        self.click(self.header.auth_btn, "кнопка Авторизация")
        self.wait_element(self.phone, "поле Телефон")

    @allure.step("Авторизация")
    def authorization(self):
        self.click_authorization()
        self.click(self.email_btn, "кнопка Войти с помощью E-mail")
        self.set_text(self.email_field, os.getenv('login'), "e-mail")
        self.set_text(self.password_field, os.getenv('password'), "пароль")
        self.click(self.login_btn, "кнопка Войти")
        self.wait_element(self.header.personal_account_btn, 'кнопка Личный кабинет')

    @allure.step("Авторизация с некорректными данными")
    def invalid_authorization(self):
        self.click_authorization()
        self.click(self.email_btn, "кнопка Войти с помощью E-mail")
        self.set_text(self.email_field, "test1234567890@test.ru", "e-mail")
        self.set_text(self.password_field, "123123", "пароль")
        self.click(self.login_btn, "кнопка Войти")
        self.wait_element(self.incorrect_login_or_password_message, "Неправильный логин или пароль")
