import allure
import pytest

from pages.main_page import MainPage


@allure.feature("Оформление заказа")
@pytest.mark.usefixtures("setup", "click_correct_city_btn", "close_cookie")
class TestPayment:

    @allure.title("Оформление заказа. Доставка курьером")
    @allure.link("https://team-cm5u.testit.software/projects/1/tests/49")
    @pytest.mark.smoke
    def test_making_order_with_courier(self):
        page = MainPage()
        page.auth.authorization()
        page.open_base_url()
        page.header.open_random_section()
        page.catalog.open_random_card()
        card_name = page.card.get_name()
        page.card.get_price()
        page.card.add_to_cart()
        page.card.open_cart()
        page.cart.checking_min_price()
        total_sum = page.cart.get_total_price()
        page.cart.click_making_order_btn()
        page.checkout.select_courier_delivery()
        page.checkout.set_address()
        delivery_price = page.checkout.select_random_courier_delivery_company()
        page.checkout.checking_total_sum(total_sum, delivery_price)
        page.checkout.set_comment()
        page.click_button('Далее')
        total_sum_with_delivery = total_sum + delivery_price
        page.checkout.checking_final_page_courier(card_name, total_sum_with_delivery)
