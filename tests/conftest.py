import allure
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


@pytest.fixture(autouse=True)
def cleanup_courier(courier_data):
    yield
    login_data = {
        "login": courier_data["login"],
        "password": courier_data["password"]
    }
    login_response = requests.post(
        'https://qa-scooter.praktikum-services.ru/api/v1/courier/login',
        json=login_data
    )
    if login_response.status_code == 200:
        courier_id = login_response.json()["id"]
        requests.delete(
            f'https://qa-scooter.praktikum-services.ru/api/v1/courier/{courier_id}'
        )


@pytest.fixture
def cleanup_order():
    track_numbers = []
    yield track_numbers
    for track in track_numbers:
        with allure.step(f"Удаление заказа с track номером {track}"):
            requests.put(
                f"https://qa-scooter.praktikum-services.ru/api/v1/orders/cancel",
                json={"track": track}
            )
