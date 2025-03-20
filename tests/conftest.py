import pytest
import requests
from courier_helper import generate_courier_data


@pytest.fixture
def base_url():
    return 'https://qa-scooter.praktikum-services.ru/api/v1/courier'


@pytest.fixture
def courier_data():
    return generate_courier_data()


@pytest.fixture
def create_courier(base_url):
    def _create_courier(data):
        response = requests.post(base_url, json=data)
        return response

    return _create_courier

@pytest.fixture
def orders_url():
    return 'https://qa-scooter.praktikum-services.ru/api/v1/orders'


@pytest.fixture
def test_order_data():
    return {
        "firstName": "Тестовый",
        "lastName": "Заказчик",
        "address": "Тестовая улица, 123",
        "metroStation": 4,
        "phone": "+7 999 888 77 66",
        "rentTime": 5,
        "deliveryDate": "2024-01-20",
        "comment": "Тестовый заказ"
    }


@pytest.fixture
def create_test_order(orders_url):
    def _create_order(order_data):
        response = requests.post(orders_url, json=order_data)
        return response

    return _create_order