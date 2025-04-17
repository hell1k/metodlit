import allure

from pages.base_page import BasePage
from pages.card_page import CardPage
from pages.cart_page import CartPage
from pages.catalog_page import CatalogPage
from pages.checkout_page import CheckoutPage
from pages.common.authorization_page import AuthorizationPage
from pages.common.header import Header


class MainPage(BasePage):

    def __init__(self):
        self.cart = CartPage()
        self.header = Header()
        self.catalog = CatalogPage()
        self.card = CardPage()
        self.auth = AuthorizationPage()
        self.checkout = CheckoutPage()

    @allure.step("Добавление в корзину рандомного товара")
    def add_to_cart_random_product(self):
        self.header.open_random_section()
        self.catalog.open_random_card()
        self.card.add_to_cart()
