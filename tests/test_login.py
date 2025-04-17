import allure
import pytest

from pages.main_page import MainPage


@allure.feature("Профиль")
@pytest.mark.usefixtures("setup", "click_correct_city_btn", "close_cookie")
class TestLogin:

    @allure.title("Авторизация с валидными данными")
    @pytest.mark.smoke
    def test_authorization(self):
        page = MainPage()
        page.auth.authorization()

    @allure.title("Авторизация с невалидными данными")
    @pytest.mark.smoke
    def test_authorization(self):
        page = MainPage()
        page.auth.invalid_authorization()
