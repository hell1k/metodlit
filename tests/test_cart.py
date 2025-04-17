import allure
import pytest

from pages.main_page import MainPage


@allure.feature("Корзина")
@pytest.mark.usefixtures("setup", "click_correct_city_btn", "close_cookie")
class TestCart:

    @allure.title("Добавление товара в корзину. Проверка данных добавленного товара")
    @pytest.mark.smoke
    def test_add_to_cart(self):
        page = MainPage()
        page.header.open_random_section()
        page.catalog.open_random_card()
        card_name = page.card.get_name()
        card_price = page.card.get_price()
        # card_article = page.card.get_article()
        page.card.add_to_cart()
        page.card.open_cart()
        page.cart.checking_product_in_cart(card_name)
        page.cart.checking_product_price(card_price)
        # page.cart.checking_article(card_article)

    @allure.title("Добавление нескольких товаров в корзину. Очистка корзины")
    @pytest.mark.smoke
    def test_add_to_cart_several_products(self):
        page = MainPage()
        cards = []
        page.add_to_cart_random_product()
        cards.append(page.card.get_name())
        page.add_to_cart_random_product()
        cards.append(page.card.get_name())
        page.card.open_cart()
        page.cart.delete_first_product()
        page.cart.checking_product_in_cart(cards[1])
        page.cart.checking_hidden_product(cards[0])
        page.cart.delete_first_product()
        page.cart.checking_hidden_product(cards[0])
        page.cart.checking_hidden_product(cards[1])
