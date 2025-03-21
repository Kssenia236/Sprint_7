import allure
import pytest

from data.test_data import OrderData
from helpers.api_helpers import CourierAPI, OrdersAPI
from helpers.courier_helper import generate_courier_data


@pytest.fixture
def authorized_courier():
    courier_data = generate_courier_data()
    with allure.step("Создание тестового курьера"):
        create_response = CourierAPI.create_courier(courier_data)
        assert create_response.status_code == 201, "Не удалось создать курьера"
    with allure.step("Авторизация курьера"):
        login_data = {
            "login": courier_data["login"],
            "password": courier_data["password"]
        }
        login_response = CourierAPI.login_courier(login_data)
        assert login_response.status_code == 200, "Не удалось авторизовать курьера"
    courier_data["id"] = login_response.json()["id"]
    yield courier_data
    with allure.step("Удаление тестового курьера"):
        CourierAPI.delete_courier(courier_data["id"])


@pytest.fixture
def created_order():
    order_data = OrderData.BASE_ORDER
    track_number = None
    with allure.step("Создание тестового заказа"):
        response = OrdersAPI.create_order(order_data)
        assert response.status_code == 201, "Не удалось создать заказ"
        track_number = response.json()["track"]
    yield {"track": track_number, "data": order_data}
    if track_number:
        with allure.step(f"Удаление тестового заказа с track номером {track_number}"):
            OrdersAPI.cancel_order(track_number)


@pytest.fixture
def new_courier_data():
    return generate_courier_data()


@pytest.fixture
def test_order_data():
    return OrderData.BASE_ORDER


@pytest.fixture
def cleanup_orders():
    track_numbers = []
    yield track_numbers
    for track in track_numbers:
        with allure.step(f"Удаление заказа с track номером {track}"):
            OrdersAPI.cancel_order(track)


@pytest.fixture
def save_track(cleanup_orders):
    def _save_track(response):
        track = response.json()["track"]
        cleanup_orders.append(track)
        return track

    return _save_track


@pytest.fixture
def login_credentials():
    def _get_credentials(courier_data):
        return {
            "login": courier_data["login"],
            "password": courier_data["password"]
        }

    return _get_credentials

@pytest.fixture
def create_test_order(test_order_data):
    response = OrdersAPI.create_order(test_order_data)
    return response.json()["track"]
