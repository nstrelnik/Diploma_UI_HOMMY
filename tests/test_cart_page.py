from pages.authorization_page import authorization
import allure
from pages.inventory_page import inventory
from pages.cart_page import cart
from pages.search_inventory import search


@allure.story('Удаление товара из корзины')
def test_delete_from_cart():
    product_name = "Ваза CRACLE"

    authorization.open_browser()

    inventory.open_catalog()
    inventory.open_product_page(product_name)
    inventory.add_product_to_cart()

    cart.open_cart()
    cart.delete_product_from_cart()
    cart.assert_delete_product_from_cart()

@allure.story('Добавление разных товаров в корзину')
def test_add_different_products():
    product_name_one = "Ваза CRACLE"
    product_name_two = "Фартук Regatta"

    authorization.open_browser()

    search.open_search()
    search.search_query_enter(product_name_one)
    search.search_query_successful(product_name_one)
    search.search_query_open_tovar()

    inventory.add_product_to_cart()

    search.open_search()
    search.search_query_enter(product_name_two)
    search.search_query_successful(product_name_two)
    search.search_query_open_tovar()

    inventory.add_product_to_cart()



    cart.open_cart()
    cart.assert_summ_products()


#@allure.story('Проверка переноса цены в корзину с детальной товара')









