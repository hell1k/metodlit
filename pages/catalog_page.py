import allure

from pages.base_page import BasePage
from selene.api import browser, s, ss

from pages.common.header import Header


class CatalogPage(BasePage):

    def __init__(self):
        self.header = Header()

    card_list = ss("//a[@class='product-card__name']/..")
    get_more_btn = s("//button[@class='get-more']")
    search_error = s("//div[@class='searchError' and contains(text(), 'Простите, товары по вашему запросу')]/span[text()='asdjkgew']")

    @allure.step("Переход в рандомную карточку")
    def open_random_card(self):
        self.wait_element(self.get_more_btn)
        random_card = self.get_random_element(self.card_list)
        self.click(random_card, self.get_element_text(random_card))

    @allure.step("Валидный запрос {query}")
    def valid_search(self, query):
        self.header.enter_search_query(query)
        with allure.step(f"Проверка первой карточки на содержание запроса {query}"):
            first_card_name = self.get_element_text(self.card_list[0]).lower()
            assert query.lower() in first_card_name, f"Название первой карточки не содержит {query}"

    @allure.step("Невалидный запрос {query}")
    def invalid_search(self, query):
        self.header.enter_search_query(query)
        with allure.step(f"Проверка наличия сообщения об ошибке поиска"):
            self.wait_element(s(f"//div[@class='searchError' and contains(text(), 'Простите, товары по вашему запросу')]/span[text()='{query}']"))



