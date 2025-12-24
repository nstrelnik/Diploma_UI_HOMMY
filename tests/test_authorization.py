import time

from pages.authorization_page import authorization
from data.users import User
import allure


@allure.title("Успешная авторизация")
@allure.story('Успешная авторизация')
def test_successful_authorization():
    user = User(
        user_email='testtest@mail.ru',
        user_password='testtest@mail.ru'
    )

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


@allure.title("Неверный логин, проверка ошибки")
@allure.story('Неверный логин, проверка ошибки')
def test_invalid_login():
    authorization.open_browser()
    authorization.click_popup()
    authorization.open_authorization_form()
    authorization.click_login()
    authorization.assert_invalid_login()


@allure.title("Неверный пароль, проверка ошибки")
@allure.story('Неверный пароль, проверка ошибки')
def test_invalid_password():
    authorization.open_browser()
    authorization.click_popup()
    authorization.open_authorization_form()
    authorization.click_login()
    authorization.assert_invalid_password()


@allure.title("Неуспешная авторизация")
@allure.story('Неуспешная авторизация')
def test_invalid_authorization():
    user = User(
        user_email='test@mail.ru',
        user_password='test@mail.ru'
    )

    authorization.open_browser()
    authorization.click_popup()
    authorization.open_authorization_form()
    (
        authorization
        .fill_username(user)
        .fill_password(user)
        .click_login()
    )
    authorization.assert_invalid_authorization()


@allure.title("Выход из аккаунта")
@allure.story('Выход из аккаунта')
def test_logout():
    user = User(
        user_email='testtest@mail.ru',
        user_password='testtest@mail.ru'
    )

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
    authorization.logout()
    authorization.asser_logout_successful()
