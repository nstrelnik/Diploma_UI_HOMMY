from selene import browser, have, be, query
import allure


class Inventory:

    @allure.step('Открытие страницы каталога')
    def open_catalog(self):
        browser.element('//*[@class = "navigation-main__list"]/li[2]').click()
        browser.element('//*[@class = "main-category__list"]/li[1]').click()
        return self

    @allure.step('Переход на страницу товара')
    def open_product_page(self, value):
        browser.all('.card-product__title').element_by(have.exact_text(value)).click()
        return self

    @allure.step('Получение остатков по товару')
    def give_kolvo(self):

        # Находим нужный ul (точное совпадение класса)
        availability_list = browser.element("ul.card-detail__availability-list")

        # Внутри ul ищем все li и извлекаем числа
        numbers = []
        for li in availability_list.all("li.card-detail__availability-list-item"):
            # Ищем span с количеством внутри текущего li
            count_span = li.element("span.card-detail__availability-count")
            text = count_span.get(query.text).strip()  # или .text

            # Извлекаем число (предполагаем формат "N шт")
            number = int(text.split()[0])  # Берём первое слово (число) до пробела
            numbers.append(number)

        # 3. Находим максимальное число
        max_quantity = max(numbers) if numbers else 0  # Если список пуст, вернёт 0
        Inventory.max_quantity = max_quantity  # Сохраняем в статическое поле
        return max_quantity
        return self

    @allure.step('Получение цены товара')
    def give_price(self):
        price_element = browser.element('div.card-detail__cost.card-product__other').element('p')

        # Получаем текст
        price = price_element.get(query.text)
        price_text = price.replace(' ', '').replace('₽', '')
        Inventory.price_text = price_text
        print(price_text)  # Выведет: "1 990₽"
        return price_text
        return self

    @allure.step('Добавление товара в корзину')
    def add_product_to_cart(self):
        browser.element('.card-product__button').click()
        return self

    @allure.step('Проверка добавления товара в корзину')
    def assert_product_to_cart_successful(self):
        browser.element('.value--add').should(be.visible)
        return self


inventory = Inventory()
