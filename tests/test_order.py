import time

from pages.authorization_page import authorization
import allure
from pages.inventory_page import inventory
from pages.cart_page import cart
from pages.search_inventory import search


@allure.story('Оформление заказа с корректными данными. НЕавторизованный пользователь. Калининград')
def test_create_order_Kaliningrad():
    product_name = "Ваза для фруктов TRINA"

    authorization.open_browser()

    search.open_search()
    search.search_query_enter(product_name)
    search.search_query_successful(product_name)
    search.search_query_open_tovar()
    inventory.give_kolvo()
    inventory.add_product_to_cart()

    cart.open_cart()
    cart.edit_quantity()
    time.sleep(1)
    cart.select_area_Kaliningrad()
    cart.select_town_Kaliningrad()
    cart.select_village_Kaliningrad()
    cart.select_pickup()
    cart.select_delivery_town()
    cart.filling_data()
    cart.personal_data()
    cart.press_create_order_button()
    time.sleep(5)
    cart.assert_create_order()

@allure.story('Проверка недоступности доставки НЕ Калининград. НЕавторизованный пользователь')
def test_create_order_not_Kaliningrad():
    product_name = "Ваза CRACLE"

    authorization.open_browser()
    authorization.click_popup()

    search.open_search()
    search.search_query_enter(product_name)
    search.search_query_successful(product_name)
    search.search_query_open_tovar()

    inventory.give_kolvo()
    inventory.add_product_to_cart()

    cart.open_cart()
    cart.select_area_not_Kaliningrad()
    cart.select_town_not_Kaliningrad()
    cart.assert_pickup_not_Kaliningrad()

    time.sleep(2)


@allure.story('Проверка суммы заказа. Калининград. Изменение кол-ва товара + Доставка')
def test_assert_order_summ_delivery():
    product_name = "Ваза CRACLE"

    authorization.open_browser()
    authorization.click_popup()

    search.open_search()
    search.search_query_enter(product_name)
    search.search_query_successful(product_name)
    search.search_query_open_tovar()

    inventory.give_kolvo()
    inventory.give_price()
    inventory.add_product_to_cart()

    cart.open_cart()
    cart.select_area_Kaliningrad()
    cart.select_town_Kaliningrad()
    cart.select_village_Kaliningrad()
    cart.select_delivery_town()

    cart.edit_quantity()
    cart.assert_order_summ_kolvo()
    cart.assert_order_summ_delivery()

@allure.story('Проверка суммы заказа. Калининград. Доставка + Изменение кол-ва товара')
def test_assert_order_summ_delivery():
    product_name = "Ваза CRACLE"

    authorization.open_browser()
    authorization.click_popup()

    search.open_search()
    search.search_query_enter(product_name)
    search.search_query_successful(product_name)
    search.search_query_open_tovar()

    inventory.give_kolvo()
    inventory.give_price()
    inventory.add_product_to_cart()

    cart.open_cart()
    cart.select_area_Kaliningrad()
    cart.select_town_Kaliningrad()
    cart.select_village_Kaliningrad()
    cart.select_delivery_town()

    cart.assert_order_summ_kolvo_and_delivery()





