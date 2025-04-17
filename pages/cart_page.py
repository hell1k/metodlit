import allure

from pages.base_page import BasePage
from pages.common.header import Header
from selene.api import s, ss


class CartPage(BasePage):

    card_name = s("//a[@class='cart-list__name']")
    cards_name = ss("//a[@class='cart-list__name']")
    card_price = s("//div[@class='cart-list__priest']/div")
    total_sum = s("//div[@class='quotation__val quotation__val--big']")
    card_article = s("//div[@class='cart-list__option' and contains(text(), 'Артикул')]")
    delete_btns = ss("//a[@class='cart-list__del']")
    empty_cart = s("//div[contains(text(), 'В корзине еще нет товаров')]")
    empty_cart_btn = s("//a[text()='Выбрать товары']")
    increase_quantity_btn = s("//div[@class='actions__plus']")
    making_order_btn = s("//button[contains(text(), 'Оформить заказ') and contains(@class, 'cart-page__btn')]")

    def __init__(self):
        self.menu = Header()

    @allure.step("Проверка наличия товара '{product_name}' в корзине")
    def checking_product_in_cart(self, product_name):
        self.wait_element(self.card_name)
        cards_title = self.get_cards_title()
        cards_title_lower = [item.lower() for item in cards_title]
        assert product_name.lower() in cards_title_lower, f"Товар {product_name} в корзине отсутствует"

    @allure.step("Проверка наличия товаров '{product_list}' в корзине")
    def checking_products_in_cart(self, product_list):
        self.wait_element(self.card_name)
        cards_title = self.get_cards_title()
        cards_title_lower = [item.lower() for item in cards_title]
        product_list_lower = [item.lower() for item in product_list]

        for i in range(len(cards_title)):
            assert cards_title_lower[i] in product_list_lower, f"{product_list[i]} не содержится в корзине"

    @allure.step("Получение названий карточек в корзине")
    def get_cards_title(self):
        self.wait_element(self.card_name)
        cards_list = []
        for i in range(len(self.cards_name)):
            cards_list.append(self.get_element_text(self.cards_name[i]))

        return cards_list

    @allure.step("Проверка цены товара '{price}'")
    def checking_product_price(self, price):
        cart_price = str(self.get_number_from_element(self.card_price))
        assert price == cart_price, f'Цена в корзине не соответствует цене в карточке.'
        'В корзине - {cart_price}. В карточке - {price}'

    @allure.step("Проверка артикула '{article}")
    def checking_article(self, card_article):
        cart_article = self.get_element_text(self.card_article).partition(": ")[2].strip()
        assert card_article == cart_article

    @allure.step("Удаление первого товара из списка")
    def delete_first_product(self):
        self.click(self.delete_btns[0])

    @allure.step("Проверка отсутствия товара '{product_name}' в корзине ")
    def checking_hidden_product(self, product_name):
        self.wait_element_hidden(s(f"//div[@class='cart-list__info']/a[contains(text(), '{product_name}')]"))

    @allure.step("Проверка пустой корзины")
    def checking_empty_cart(self):
        self.wait_element(self.empty_cart, "В корзине еще нет товаров")
        self.wait_element(self.empty_cart_btn, "кнопка Выбрать товары")

    @allure.step("Проверка на сумму минимального заказа")
    def checking_min_price(self):
        cart_price = self.get_number_from_element(self.total_sum)
        counter = 1
        while cart_price < 550:
            with allure.step("Увеличение количества товаров в корзине"):
                self.click(self.increase_quantity_btn, "кнопка увеличения количества товара '+'")
                self.wait_a_moment()
                counter += 1
                self.wait_element(s(f"//div[@class='quotation__name quotation__name--big' and contains(text(), '{str(counter)}')]"), f"количество товаров - {counter}")
                cart_price = self.get_number_from_element(self.total_sum)

    @allure.step("Клик по кнопке Оформить заказ")
    def click_making_order_btn(self):
        self.click(self.making_order_btn)
        self.checking_text("Доставка и оплата")

    def get_total_price(self):
        return self.get_number_from_element(self.total_sum)
