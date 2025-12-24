import time

from selene import browser, have, be, query, by
import allure
import time
from selene.support.shared import browser
from selenium.webdriver.common.keys import Keys# Импортируем функцию из вашего файла
from pages.inventory_page import Inventory






class Cart:

    @allure.step('Переход на страницу корзины')
    def open_cart(self):
        browser.element('//*[@class = "navigation-personal"]/li[4]').click()
        return self

    @allure.step('Удаление товара из корзины')
    def delete_product_from_cart(self):
        browser.element('.ordered-products__product-delete').click()
        return self

    @allure.step('Проверка удаления товара из корзины')
    def assert_delete_product_from_cart(self):
        browser.element('.cart__empty-block-text').should(be.visible).should(have.text("В вашей корзине пока пусто"))
        return self

    @allure.step('Выбор Калининградской области в блоке "Регион"')
    def select_area_Kaliningrad(self):

        browser.all('.cart__step-item-title').element_by(have.exact_text('Регион доставки'))
        delivery_region_block = browser.all('.cart__step-item-title').element_by(
            have.exact_text('Регион доставки')
        )

        browser.execute_script("arguments[0].scrollIntoView();", delivery_region_block.locate())
        delivery_region_block.s('.bx-ui-combobox-toggle')
        browser.all('//*[contains(@class, "bx-ui-combobox-toggle")]')[1].click()
        element1 = browser.all('//*[contains(@class, "bx-ui-combobox-toggle")]')[1]
        element1.click()

        region_name = "Калининградская область"
        try:
            region = browser.element(f'//div[@class="bx-ui-combobox-variant" and .="{region_name}"]')
            region.click()
            print(f"Регион '{region_name}' успешно выбран")
        except Exception:
            print(f"Регион '{region_name}' не найден в DOM")

        start_time = time.time()
        while time.time() - start_time < 10:
            all_options = browser.all('.bx-ui-combobox-variant')
            if all_options:
                break
            time.sleep(0.5)
        else:
            raise ValueError("Элементы не загрузились за 10 секунд")

        print(f"Найдено элементов: {len(all_options)}")
        for i, element in enumerate(all_options, 1):
            element_text = browser.execute_script("return arguments[0].textContent", element.locate())
            print(f"{i}. {element_text}")

        last_option = all_options[-1]
        last_text = browser.execute_script("return arguments[0].textContent", last_option.locate())
        print(f"\nПоследний элемент: '{last_text}'")

        scroll_container = browser.all('.bx-ui-combobox-dropdown')[1]

        browser.execute_script("""
            arguments[0].style.border = '2px solid red';
            arguments[0].style.overflowY = 'scroll';  // Принудительно включаем скролл
        """, scroll_container.locate())

        def scroll_to_element(target_element_text, max_attempts=15):
            scroll_container = browser.all('.bx-ui-combobox-dropdown')[1]

            last_height = 0
            attempts = 0
            element_found = False

            while attempts < max_attempts and not element_found:
                attempts += 1

                current_height = browser.execute_script(
                    "return arguments[0].scrollHeight",
                    scroll_container.locate()
                )

                browser.execute_script("""
                    arguments[0].scrollTop = arguments[0].scrollHeight;
                """, scroll_container.locate())

                print(f"🔄 Попытка {attempts}: Прокрутка до {current_height}px")
                time.sleep(1)

                all_elements = browser.all('.bx-ui-combobox-variant')
                for element in all_elements:
                    element_text = browser.execute_script(
                        "return arguments[0].textContent",
                        element.locate()
                    )
                    if target_element_text in element_text:
                        target_element = element
                        element_found = True
                        print(f"🔍 Найден элемент: '{element_text.strip()}'")
                        break

                if current_height == last_height and not element_found:
                    print("Новые элементы не загружаются")
                    break

                last_height = current_height

            if element_found:
                browser.execute_script("""
                    const container = arguments[0];
                    const element = arguments[1];
                    container.scrollTop = element.offsetTop - container.offsetTop - 100;
                """, scroll_container.locate(), target_element.locate())

                print(f"\n🎯 Элемент '{target_element_text}' успешно отображен")
                return True
            else:
                print(f"\n⚠️ Элемент '{target_element_text}' не найден после {max_attempts} попыток")
                return False

        # Пример использования:
        scroll_to_element("Калининградская область")  # Ищем элемент содержащий текст "Москва"

        browser.all('.bx-ui-combobox-variant').element_by(have.exact_text('Калининградская область')).click()
        return self

    @allure.step('Заполнение списка')
    def select_town_Kaliningrad(self):
        # второй выпадающий список

        element2 = browser.all('//*[contains(@class, "bx-ui-combobox-toggle")]')[2]
        element2.click()

        def scroll_to_element(target_element_text, max_attempts=15):
            # 1. Находим контейнер
            scroll_container = browser.all('.bx-ui-combobox-dropdown')[2]

            # 2. Инициализация
            last_height = 0
            attempts = 0
            element_found = False

            while attempts < max_attempts and not element_found:
                attempts += 1

                # 3. Получаем текущую высоту
                current_height = browser.execute_script(
                    "return arguments[0].scrollHeight",
                    scroll_container.locate()
                )

                # 4. Прокручиваем с анимацией
                browser.execute_script("""
                    arguments[0].scrollTop = arguments[0].scrollHeight;
                """, scroll_container.locate())

                print(f"🔄 Попытка {attempts}: Прокрутка до {current_height}px")
                time.sleep(1)  # Ждем подгрузки

                # 5. Проверяем наличие элемента (все элементы, включая невидимые)
                all_elements = browser.all('.bx-ui-combobox-variant')
                for element in all_elements:
                    element_text = browser.execute_script(
                        "return arguments[0].textContent",
                        element.locate()
                    )
                    if target_element_text in element_text:
                        target_element = element
                        element_found = True
                        print(f"🔍 Найден элемент: '{element_text.strip()}'")
                        break

                # 6. Если высота не изменилась - выходим
                if current_height == last_height and not element_found:
                    print("Новые элементы не загружаются")
                    break

                last_height = current_height

            # 7. Финальные действия
            if element_found:
                # Прокручиваем элемент в видимую область
                browser.execute_script("""
                    const container = arguments[0];
                    const element = arguments[1];
                    container.scrollTop = element.offsetTop - container.offsetTop - 100;
                """, scroll_container.locate(), target_element.locate())

                print(f"\n🎯 Элемент '{target_element_text}' успешно отображен")
                return True
            else:
                print(f"\n⚠️ Элемент '{target_element_text}' не найден после {max_attempts} попыток")
                return False

        # Пример использования:
        scroll_to_element("Калининград")  # Ищем элемент содержащий текст "Москва"

        browser.all('.bx-ui-combobox-variant').element_by(have.exact_text('Калининград')).click()

        return self

    @allure.step('Выбор НЕ Калининградской области')
    def select_area_not_Kaliningrad(self):
        browser.all('.cart__step-item-title').element_by(have.exact_text('Регион доставки'))
        delivery_region_block = browser.all('.cart__step-item-title').element_by(
            have.exact_text('Регион доставки')
        )

        browser.execute_script("arguments[0].scrollIntoView();", delivery_region_block.locate())
        delivery_region_block.s('.bx-ui-combobox-toggle')
        browser.all('//*[contains(@class, "bx-ui-combobox-toggle")]')[1].click()
        element1 = browser.all('//*[contains(@class, "bx-ui-combobox-toggle")]')[1]
        element1.click()

        region_name = "Амурская область"
        try:
            region = browser.element(f'//div[@class="bx-ui-combobox-variant" and .="{region_name}"]')
            region.click()
            print(f"Регион '{region_name}' успешно выбран")
            return self  # Выходим из функции, если регион уже выбран
        except Exception:
            print(f"Регион '{region_name}' не найден в DOM")

        start_time = time.time()
        while time.time() - start_time < 10:
            all_options = browser.all('.bx-ui-combobox-variant')
            if all_options:
                break
            time.sleep(0.5)
        else:
            raise ValueError("Элементы не загрузились за 10 секунд")

        print(f"Найдено элементов: {len(all_options)}")
        for i, element in enumerate(all_options, 1):
            element_text = browser.execute_script("return arguments[0].textContent", element.locate())
            print(f"{i}. {element_text}")

        last_option = all_options[-1]
        last_text = browser.execute_script("return arguments[0].textContent", last_option.locate())
        print(f"\nПоследний элемент: '{last_text}'")

        scroll_container = browser.all('.bx-ui-combobox-dropdown')[1]

        browser.execute_script("""
                    arguments[0].style.border = '2px solid red';
                    arguments[0].style.overflowY = 'scroll';  // Принудительно включаем скролл
                """, scroll_container.locate())

        def scroll_to_element(target_element_text, max_attempts=15):
            scroll_container = browser.all('.bx-ui-combobox-dropdown')[1]

            last_height = 0
            attempts = 0
            element_found = False

            while attempts < max_attempts and not element_found:
                attempts += 1

                current_height = browser.execute_script(
                    "return arguments[0].scrollHeight",
                    scroll_container.locate()
                )

                browser.execute_script("""
                            arguments[0].scrollTop = arguments[0].scrollHeight;
                        """, scroll_container.locate())

                print(f"🔄 Попытка {attempts}: Прокрутка до {current_height}px")
                time.sleep(1)

                all_elements = browser.all('.bx-ui-combobox-variant')
                for element in all_elements:
                    element_text = browser.execute_script(
                        "return arguments[0].textContent",
                        element.locate()
                    )
                    if target_element_text in element_text:
                        target_element = element
                        element_found = True
                        print(f"🔍 Найден элемент: '{element_text.strip()}'")
                        break

                if current_height == last_height and not element_found:
                    print("Новые элементы не загружаются")
                    break

                last_height = current_height

            if element_found:
                browser.execute_script("""
                            const container = arguments[0];
                            const element = arguments[1];
                            container.scrollTop = element.offsetTop - container.offsetTop - 100;
                        """, scroll_container.locate(), target_element.locate())

                print(f"\n🎯 Элемент '{target_element_text}' успешно отображен")
                return True
            else:
                print(f"\n⚠️ Элемент '{target_element_text}' не найден после {max_attempts} попыток")
                return False

        # Пример использования:
        scroll_to_element("Амурская область")  # Ищем элемент содержащий текст "Москва"

        browser.all('.bx-ui-combobox-variant').element_by(have.exact_text('Амурская область')).click()
        return self

    @allure.step('Заполнение списка')
    def select_town_not_Kaliningrad(self):
        # второй выпадающий список

        element2 = browser.all('//*[contains(@class, "bx-ui-combobox-toggle")]')[2]
        element2.click()

        def scroll_to_element(target_element_text, max_attempts=15):
            # 1. Находим контейнер
            scroll_container = browser.all('.bx-ui-combobox-dropdown')[2]

            # 2. Инициализация
            last_height = 0
            attempts = 0
            element_found = False

            while attempts < max_attempts and not element_found:
                attempts += 1

                # 3. Получаем текущую высоту
                current_height = browser.execute_script(
                    "return arguments[0].scrollHeight",
                    scroll_container.locate()
                )

                # 4. Прокручиваем с анимацией
                browser.execute_script("""
                        arguments[0].scrollTop = arguments[0].scrollHeight;
                    """, scroll_container.locate())

                print(f"🔄 Попытка {attempts}: Прокрутка до {current_height}px")
                time.sleep(1)  # Ждем подгрузки

                # 5. Проверяем наличие элемента (все элементы, включая невидимые)
                all_elements = browser.all('.bx-ui-combobox-variant')
                for element in all_elements:
                    element_text = browser.execute_script(
                        "return arguments[0].textContent",
                        element.locate()
                    )
                    if target_element_text in element_text:
                        target_element = element
                        element_found = True
                        print(f"🔍 Найден элемент: '{element_text.strip()}'")
                        break

                # 6. Если высота не изменилась - выходим
                if current_height == last_height and not element_found:
                    print("Новые элементы не загружаются")
                    break

                last_height = current_height

            # 7. Финальные действия
            if element_found:
                # Прокручиваем элемент в видимую область
                browser.execute_script("""
                        const container = arguments[0];
                        const element = arguments[1];
                        container.scrollTop = element.offsetTop - container.offsetTop - 100;
                    """, scroll_container.locate(), target_element.locate())

                print(f"\n🎯 Элемент '{target_element_text}' успешно отображен")
                return True
            else:
                print(f"\n⚠️ Элемент '{target_element_text}' не найден после {max_attempts} попыток")
                return False

        # Пример использования:
        scroll_to_element("Белогорск")  # Ищем элемент содержащий текст "Москва"

        browser.all('.bx-ui-combobox-variant').element_by(have.exact_text('Белогорск')).click()

        return self

    @allure.step('Заполнение села для Калининграда')
    def select_village_Kaliningrad(self):
        # второй выпадающий список

        element2 = browser.all('//*[contains(@class, "bx-ui-combobox-toggle")]')[3]
        element2.click()

        def scroll_to_element(target_element_text, max_attempts=15):
            # 1. Находим контейнер
            scroll_container = browser.all('.bx-ui-combobox-dropdown')[3]

            # 2. Инициализация
            last_height = 0
            attempts = 0
            element_found = False

            while attempts < max_attempts and not element_found:
                attempts += 1

                # 3. Получаем текущую высоту
                current_height = browser.execute_script(
                    "return arguments[0].scrollHeight",
                    scroll_container.locate()
                )

                # 4. Прокручиваем с анимацией
                browser.execute_script("""
                            arguments[0].scrollTop = arguments[0].scrollHeight;
                        """, scroll_container.locate())

                print(f"🔄 Попытка {attempts}: Прокрутка до {current_height}px")
                time.sleep(1)  # Ждем подгрузки

                # 5. Проверяем наличие элемента (все элементы, включая невидимые)
                all_elements = browser.all('.bx-ui-combobox-variant')
                for element in all_elements:
                    element_text = browser.execute_script(
                        "return arguments[0].textContent",
                        element.locate()
                    )
                    if target_element_text in element_text:
                        target_element = element
                        element_found = True
                        print(f"🔍 Найден элемент: '{element_text.strip()}'")
                        break

                # 6. Если высота не изменилась - выходим
                if current_height == last_height and not element_found:
                    print("Новые элементы не загружаются")
                    break

                last_height = current_height

            # 7. Финальные действия
            if element_found:
                # Прокручиваем элемент в видимую область
                browser.execute_script("""
                            const container = arguments[0];
                            const element = arguments[1];
                            container.scrollTop = element.offsetTop - container.offsetTop - 100;
                        """, scroll_container.locate(), target_element.locate())

                print(f"\n🎯 Элемент '{target_element_text}' успешно отображен")
                return True
            else:
                print(f"\n⚠️ Элемент '{target_element_text}' не найден после {max_attempts} попыток")
                return False

        # Пример использования:
        scroll_to_element("Август снт")  # Ищем элемент содержащий текст "Москва"

        browser.all('.bx-ui-combobox-variant').element_by(have.exact_text('Август снт')).click()

        return self

    @allure.step('Выбор доставки по выбранному городу')
    def select_delivery_town(self):
        give_town_text = browser.all(".bx-ui-combobox-fake.bx-combobox-fake-as-input")[1]
        town_textext = give_town_text.get(query.text)

        print("Извлечённый текст:", town_textext)
        # time.sleep(10)

        delivery_town = (
            browser.all(".cart__order-delivery")
            .element_by(have.exact_text(town_textext))
            .should(be.visible)
        )

        # Переходим к родительскому элементу с помощью XPath
        delivery_label = delivery_town.element("./..")

        # Ищем стоимость доставки внутри родителя
        delivery_cost = delivery_label.element(".cart__order-delivery-cost")
        delivery_cost_text = delivery_cost.get(query.text)

        print("Стоимость доставки:", delivery_cost_text)

        # Преобразуем в число
        #delivery_cost_summ = int(delivery_cost_text.replace(' ₽', '').replace(' ', ''))
        self.delivery_cost_summ = int(delivery_cost_text.replace(' ₽', '').replace(' ', ''))
        print("Стоимость доставки как число:", self.delivery_cost_summ)

        print(delivery_town.get(query.text))
        delivery_town.click()
        time.sleep(5)
        return self

    @allure.step('Выбор самовывоза')
    def select_pickup(self):
        browser.element('.cart__order-delivery').should(have.text('Самовывоз')).click()
        return self

    @allure.step('Заполнение информации о покупателе')
    def filling_data(self):
        FIO = browser.element('[name="ORDER_PROP_3"]')
        FIO.type("Тестовый пользователь")
        Email = browser.element('[name="ORDER_PROP_4"]')
        Email.type("test@mail.ru")
        Tel = browser.element('[name="ORDER_PROP_5"]')
        Tel.type("79216088034").press(Keys.ENTER)
        Comment = browser.element('[name="ORDER_DESCRIPTION"]').click()
        Adress = browser.element('[name="ORDER_PROP_6"]')
        Adress.type("Тестовый адрес")
        time.sleep(2)
        Comment.type('Тестовый комментарий')
        return self

    @allure.step('Заполнение согласия на обработку ПД')
    def personal_data(self):
        browser.element(by.text("Согласен на обработку персональных данных")).click()
        browser.element(by.text("Принимаю")).click()
        return self

    @allure.step('Отмена согласия на обработку ПД')
    def no_personal_data(self):
        browser.element(by.text("Согласен на обработку персональных данных")).click()
        browser.element(by.text("Не принимаю")).click()
        return self

    @allure.step('Изменение кол-ва товара через input и сравнение с максимально допустимым')
    def edit_quantity(self):
        input_field = browser.element('[data-entity="basket-item-quantity-field"]')

        # Вариант: Backspace
        (input_field
         .click()
         .press(Keys.BACKSPACE)  # Удаляем последний символ
         .press(Keys.BACKSPACE)  # Если было "10", удаляем "0", потом "1"
         .type("200")  # Вводим новое значение
         .press(Keys.ENTER))  # Подтверждаем ввод
        time.sleep(2)
        print(f"Максимальное количество: {Inventory.max_quantity}")
        max_kolvo = Inventory.max_quantity
        current_value = input_field.get(query.value)
        assert int(current_value) == max_kolvo, \
            f"Количество не совпадает! Ожидалось: {max_kolvo}, Фактическое: {current_value}"

        return current_value


    @allure.step('Проверка суммы при выборе кол-ва товаров и доставки')
    def assert_order_summ_kolvo_and_delivery(self):
        #получение суммы за товары
        value_element = browser.element(
            '//td[@class="ordered-products__field" and contains(text(), "Товаров на сумму:")]/following-sibling::td[@class="ordered-products__value"]')

        total_amount = value_element.get(query.text).replace(' ', '').replace('₽', '')
        print(f"Товаров на сумму: {total_amount}")

        summ_order_tovar = int(Inventory.price_text) * int(Inventory.max_quantity)

        assert int(summ_order_tovar) == int(total_amount), \
            f"Суммы не совпадают! Ожидалось: {summ_order_tovar}, Фактическое: {total_amount}"

        summ_order_tovar_delivery = self.delivery_cost_summ + int(summ_order_tovar)

        value_element_2 = browser.element(
            '//td[@class="ordered-products__field" and contains(text(), "Итого:")]/following-sibling::td[@class="ordered-products__value"]')

        total_amount_2 = value_element_2.get(query.text).replace(' ', '').replace('₽', '')
        print(f"Итого: {total_amount_2}")

        assert int(summ_order_tovar_delivery) == int(total_amount_2), \
            f"Суммы не совпадают! Ожидалось: {summ_order_tovar_delivery}, Фактическое: {total_amount_2}"
        print(summ_order_tovar_delivery)


        return self


    @allure.step('Проверка суммы при выборе кол-ва товаров и доставки')
    def assert_order_summ_delivery(self):
        #получение суммы за товары
        value_element = browser.element(
            '//td[@class="ordered-products__field" and contains(text(), "Товаров на сумму:")]/following-sibling::td[@class="ordered-products__value"]')

        total_amount = value_element.get(query.text).replace(' ', '').replace('₽', '')
        print(f"Товаров на сумму: {total_amount}")


        summ_order_tovar_delivery = self.delivery_cost_summ + int(total_amount)

        value_element_2 = browser.element(
            '//td[@class="ordered-products__field" and contains(text(), "Итого:")]/following-sibling::td[@class="ordered-products__value"]')

        total_amount_2 = value_element_2.get(query.text).replace(' ', '').replace('₽', '')
        print(f"Итого: {total_amount_2}")

        assert int(summ_order_tovar_delivery) == int(total_amount_2), \
            f"Суммы не совпадают! Ожидалось: {summ_order_tovar_delivery}, Фактическое: {total_amount_2}"
        print(summ_order_tovar_delivery)

        return self

    @allure.step('Проверка суммы при выборе кол-ва товаров и доставки')
    def assert_order_summ_kolvo(self):
        # получение суммы за товары
        value_element = browser.element(
            '//td[@class="ordered-products__field" and contains(text(), "Товаров на сумму:")]/following-sibling::td[@class="ordered-products__value"]')

        total_amount = value_element.get(query.text).replace(' ', '').replace('₽', '')
        print(f"Товаров на сумму: {total_amount}")

        summ_order_tovar = int(Inventory.price_text) * int(Inventory.max_quantity)

        assert int(summ_order_tovar) == int(total_amount), \
            f"Суммы не совпадают! Ожидалось: {summ_order_tovar}, Фактическое: {total_amount}"

        return self

    # @allure.step('Проверка суммы товаров если несколько разных позиций')
    # def assert_summ_products(self):
    #     # получение суммы за товары
    #     value_element = browser.element(
    #         '//td[@class="ordered-products__field" and contains(text(), "Товаров на сумму:")]/following-sibling::td[@class="ordered-products__value"]')
    #
    #     total_amount = value_element.get(query.text).replace(' ', '').replace('₽', '')
    #     print(f"Товаров на сумму: {total_amount}")
    #
    #     print(Inventory.price_text)
    #
    #     return self


    #@allure.step('Получение цены товара в корзине')





    @allure.step('Поиск и выбор доставки в город')
    def delivery_Kaliningrad(self):
        browser.all('p.cart__order-delivery').element_by(have.exact_text('Калининград')).click()


    @allure.step('Клик по кнопке создания заказа')
    def press_create_order_button(self):
        browser.element('.cart__order-button-finish.button').click()
        return self



    @allure.step('Проверка на создание заказа')
    def assert_create_order(self):
        assert browser.element('.cart__order-title').should(be.visible).should(have.text('успешно создан'))
        return self

    @allure.step('Проверка недоступности доставки НЕ для Калининграда')
    def assert_pickup_not_Kaliningrad(self):
        assert browser.element('.cart__order-delivery').should(have.text('Стоимость доставки будет предоставлена позже (Ошибка: У товаров не задан вес!)')).click()
        return self

cart = Cart()
