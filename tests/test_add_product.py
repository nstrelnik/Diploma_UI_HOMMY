from pages.authorization_page import authorization
from pages.inventory_page import inventory
from pages.search_inventory import search
from pages.favorite_page import favorite
from data.users import User
from pages.cart_page import cart
import allure


@allure.story('Добавление товара в корзину пользователя')
def test_add_product_to_cart():
    user = User(
        user_email='testtest@mail.ru',
        user_password='testtest@mail.ru'
    )
    product_name = "Подсвечник Montone M"

    authorization.open_browser()
    authorization.click_popup()
    authorization.open_authorization_form()
    (
        authorization
        .fill_username(user)
        .fill_password(user)
        .click_login()
    )
    authorization.assert_successful_authorization()

    inventory.open_catalog()
    inventory.open_product_page(product_name)
    inventory.add_product_to_cart()
    inventory.assert_product_to_cart_successful()

    cart.open_cart()
    cart.delete_product_from_cart()


@allure.story('Добавление товара в Избранное пользователя')
def test_add_product_to_favorite():
    user = User(
        user_email='testtest@mail.ru',
        user_password='testtest@mail.ru'
    )
    product_name = "Подсвечник Montone M"

    authorization.open_browser()
    authorization.click_popup()
    authorization.open_authorization_form()
    (
        authorization
        .fill_username(user)
        .fill_password(user)
        .click_login()
    )
    authorization.assert_successful_authorization()

    inventory.open_catalog()

    favorite.open_page_product_for_favorite(product_name)
    favorite.add_product_to_favorites()
    favorite.open_page_favorite()
    favorite.assert_product_to_favorites_successful(product_name)
    favorite.delete_product_from_favorite()


@allure.story('Поиск товара в каталоге через строку поиска')
def test_search():
    product_name = "Ваза CRACLE"

    authorization.open_browser()

    authorization.click_popup()

    search.open_search()
    search.search_query_enter(product_name)
    search.search_query_successful(product_name)






