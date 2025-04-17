import allure
import pytest

from pages.main_page import MainPage


@allure.feature("Поиск")
@pytest.mark.usefixtures("setup", "click_correct_city_btn", "close_cookie")
class TestSearch:

    @allure.title("Валидный поиск")
    @pytest.mark.smoke
    def test_successfully_search(self):
        page = MainPage()
        page.catalog.valid_search('Биология')

    @allure.title("Невалидный поиск")
    @pytest.mark.smoke
    def test_invalid_search(self):
        page = MainPage()
        page.catalog.invalid_search('asdjkgew')

