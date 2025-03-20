import allure
import pytest
import requests


class TestCreateOrder:

    @allure.title("Проверка создания заказа с разными цветами")
    @pytest.mark.parametrize("color", [["BLACK"], ["GREY"], ["BLACK", "GREY"], []])
    def test_create_order_with_colors(self, color, cleanup_order):
        order_data = {
            "firstName": "Тестовый",
            "lastName": "Заказчик",
            "address": "Тестовая улица, 123",
            "metroStation": 4,
            "phone": "+7 999 888 77 66",
            "rentTime": 5,
            "deliveryDate": "2024-01-20",
            "comment": "Тестовый заказ",
            "color": color
        }

        with allure.step("Отправка запроса на создание заказа"):
            response = requests.post("https://qa-scooter.praktikum-services.ru/api/v1/orders",
                                     json=order_data)

        with allure.step("Проверка, что статус-код ответа равен 201"):
            assert response.status_code == 201

        with allure.step("Проверка, что в теле ответа содержится track"):
            response_data = response.json()
            assert "track" in response_data
            assert isinstance(response_data["track"], int)
            cleanup_order.append(response_data["track"])

    @allure.title("Проверка наличия track в ответе при создании заказа")
    @pytest.mark.parametrize("order_data", [
        {
            "firstName": "Тестовый",
            "lastName": "Заказчик",
            "address": "Тестовая улица, 123",
            "metroStation": 4,
            "phone": "+7 999 888 77 66",
            "rentTime": 5,
            "deliveryDate": "2024-01-20",
            "comment": "Тестовый заказ",
            "color": ["BLACK", "GREY"]
        },
        {
            "firstName": "Тестовый",
            "lastName": "Заказчик",
            "address": "Тестовая улица, 123",
            "metroStation": 4,
            "phone": "+7 999 888 77 66",
            "rentTime": 5,
            "deliveryDate": "2024-01-20",
            "comment": "Тестовый заказ"
        }
    ])
    def test_order_response_contains_track(self, order_data, cleanup_order):
        with allure.step("Отправка запроса на создание заказа"):
            response = requests.post("https://qa-scooter.praktikum-services.ru/api/v1/orders",
                                     json=order_data)

        with allure.step("Проверка, что статус-код ответа равен 201"):
            assert response.status_code == 201

        with allure.step("Проверка, что в теле ответа содержится track и он больше 0"):
            response_data = response.json()
            assert "track" in response_data
            assert isinstance(response_data["track"], int)
            assert response_data["track"] > 0
            cleanup_order.append(response_data["track"])

