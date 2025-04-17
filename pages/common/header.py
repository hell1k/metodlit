import allure

from pages.base_page import BasePage
from selene.api import s, ss


class Header(BasePage):

    menu_list = ss("//span[@class='carousel-item__item']/a")
    basket_counter = s("//div[@class='cart__icon']/div[@class='cart__col']")
    search_input = s("//input[@id='searchInput']")
    search_btn = s("//button[@class='search__btn']")
    breadcrumb_search = s("//ul[@class='breadcrumb']//span[text()='Поиск']")
    auth_btn = s("//div[@class='login__val' and contains(text(), 'Авторизация')]")
    personal_account_btn = s("//div[@class='login__val' and contains(text(), 'Личный кабинет')]")

    @allure.step("Переход в рандомный раздел")
    def open_random_section(self):
        random_section = self.get_random_element(self.menu_list)
        self.click(random_section, self.get_element_text(random_section))

    @allure.step("Проверка отображения числа '{counter}' на иконке корзины")
    def checking_basket_counter(self, counter):
        self.checking_presence_of_element(s(f"//div[@class='cart__icon']/div[@class='cart__col' and text()='{counter}']"))

    @allure.step("Ввод поискового запроса '{query}'")
    def enter_search_query(self, query):
        self.set_text(self.search_input, query, "поиск")
        self.click(self.search_btn, 'кнопка поиска')
        self.wait_element(self.breadcrumb_search)


