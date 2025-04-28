import allure
import pytest

from pages.main_page import MainPage


@allure.feature("Профиль")
@pytest.mark.usefixtures("setup", "click_correct_city_btn", "close_cookie")
class TestLogin:

    @allure.title("Авторизация с невалидными данными")
    @allure.link("https://team-cm5u.testit.software/projects/1/tests/52")
    @pytest.mark.smoke
    def test_invalid_authorization(self):
        page = MainPage()
        page.auth.invalid_authorization()
