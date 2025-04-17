import allure
import pytest

from pages.main_page import MainPage


@allure.feature("Оформление заказа")
@pytest.mark.usefixtures("setup", "click_correct_city_btn", "close_cookie")
class TestPayment:

    def test_making_order_with_courier(self):
        page = MainPage()
        page.auth.authorization()
        page.header.open_random_section()
        page.catalog.open_random_card()
        page.card.get_name()
        page.card.get_price()
        page.card.add_to_cart()
        page.card.open_cart()
        page.cart.checking_min_price()
        total_sum = page.cart.get_total_price()
        page.cart.click_making_order_btn()
        page.checkout.select_courier_delivery()
        page.checkout.select_random_courier_delivery_company()
        delivery_price = page.checkout.select_random_courier_delivery_company()
        page.checkout.checking_total_sum(total_sum, delivery_price)
        page.checkout.set_comment()
        print()
