import allure
import faker

from pages.base_page import BasePage
from selene.api import browser, s, ss


class CheckoutPage(BasePage):
    goods_price = s("(//div[@class='quotation__val'])[1]")
    total_sum = s("//div[@class='quotation__val quotation__val--big']")
    delivery_price = s("//div[@class='quotation__name ' and contains(text(), 'Доставка')]/following-sibling::div")
    courier_delivery_btn = s("//span[contains(text(), 'Доставка курьером')]")
    courier_delivery_list = ss("//label[contains(@for, 'choice-courierType')]")
    comment_field = s("//textarea[@name='Model.comment']")
    street = s("//input[@name='street']")
    home = s("//input[@name='home']")
    housing = s("//input[@name='housing']")
    entrance = s("//input[@name='entrance']")
    flat = s("//input[@name='flat']")
    intercom = s("//input[@name='intercom']")
    index = s("//input[@name='index']")
    cart_list_info = s("//div[@class='cart-list__info']/a")
    agreement_checkbox = s("//label[@for='agreemnt']")

    def get_delivery_price(self):
        return self.get_number_from_element(self.delivery_price)

    def get_total_sum(self):
        return self.get_number_from_element(self.total_sum)

    def get_goods_price(self):
        return self.get_number_from_element(self.goods_price)

    @allure.step("Выбор Доставка курьером")
    def select_courier_delivery(self):
        self.click(self.courier_delivery_btn)
        self.checking_text("Курьерская доставка")

    @allure.step("Выбор рандомной курьерской службы")
    def select_random_courier_delivery_company(self):
        random_element = self.get_random_element(self.courier_delivery_list)
        delivery_price = self.get_number_from_string(self.get_element_text(random_element).partition('Цена:')[2])
        self.click(random_element)
        self.wait_a_second()
        return delivery_price

    @allure.step("Проверка итоговой суммы")
    def checking_total_sum(self, goods_price, delivery_price):
        assert self.get_number_from_element(self.total_sum) == goods_price + delivery_price, f"Итоговая сумма ({str(self.get_number_from_element(self.total_sum))}) не равна сумме заказов ({str(goods_price)}) + сумма доставки ({str(delivery_price)})."

    @allure.step("Добавление комментария")
    def set_comment(self):
        self.set_text(self.comment_field, faker.Faker().text())

    @allure.step("Добавление адреса")
    def set_address(self):
        self.click_button("Добавить адрес доставки")
        self.set_text(self.street, 'Пушкина', 'улица')
        self.set_text(self.home, '1', 'Дом')
        self.set_text(self.housing, '1', 'Кор./стр.')
        self.set_text(self.entrance, '1', 'Подъезд')
        self.set_text(self.flat, '1', 'Квартира')
        self.set_text(self.intercom, '1', 'Домофон')
        self.set_text(self.index, '123456', 'Индекс')
        self.click_button("Сохранить")
        self.checking_text("Пушкина, д. 1, стр. 1, под. 1, кв. 1, домофон 1")
        self.click(s('//span[contains(text(), "Пушкина, д. 1, стр. 1, под. 1, кв. 1, домофон 1")]'))

    @allure.step("Проверка данных на странице Проверка")
    def checking_final_page_courier(self, card_name, total_sum):
        with allure.step(f"Проверка наличия товара '{card_name}'"):
            assert card_name in self.get_element_text(self.cart_list_info), "Название карточки не соответствует названию в чекауте"
        self.checking_text("Тестов")
        self.checking_text("Тест")
        self.checking_text("79237079068")
        self.checking_text("hell1k@yandex.ru")
        self.checking_text("Курьер")
        self.checking_text("Банковской картой онлайн")
        self.checking_text("Пушкина, д. 1, стр. 1, под. 1, кв. 1, домофон 1")
        assert total_sum == self.get_number_from_element(self.total_sum), f"Итоговая сумма на странице Проверка не соответствует {total_sum}"
        with allure.step("Проверка неактивной кнопки 'Проверить заказа и оплатить'"):
            assert 'disable' in self.get_attribute(self.get_button("Проверить заказ и оплатить"), 'class'), "Кнопка 'Проверить заказа и оплатить' активна"
        self.click(self.agreement_checkbox, "чекбокс пользовательского соглашения")
        self.wait_a_second()
        with allure.step("Проверка активной кнопки 'Проверить заказа и оплатить'"):
            assert 'disable' not in self.get_attribute(self.get_button("Проверить заказ и оплатить"), 'class'), "Кнопка 'Проверить заказа и оплатить' не активна"

