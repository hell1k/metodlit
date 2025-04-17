import allure

from pages.base_page import BasePage
from selene.api import browser, s, ss


class CardPage(BasePage):

    name = s("//h1[@itemprop='name']")
    price = s("//meta[@itemprop='price']")
    add_to_cart_btn = s("//a[contains(@class, 'btn-green-solid-big') and (contains(text(), 'Добавить в корзину') or contains(text(), 'Купить'))]")
    in_the_basket_btn = s("//a[@href='/cart' and contains(text(), 'В корзине')]")
    article = s("//div[@id='Артикул']")

    def get_name(self):
        return self.get_element_text(self.name)

    def get_price(self):
        return self.get_attribute(self.price, 'content')

    @allure.step("Клик по кнопке Добавить в корзину")
    def add_to_cart(self):
        self.click(self.add_to_cart_btn, "кнопка Добавить в корзину")
        self.wait_element(self.in_the_basket_btn, "кнопка В корзине")

    @allure.step("Переход в корзину")
    def open_cart(self):
        self.click(self.in_the_basket_btn)

    def get_article(self):
        self.get_element_text(self.article)

