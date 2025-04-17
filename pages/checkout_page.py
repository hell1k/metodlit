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
