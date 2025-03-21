import allure
import requests
from data.urls import *


class CourierAPI:
    @staticmethod
    @allure.step("Создание курьера")
    def create_courier(courier_data: dict) -> requests.Response:
        return requests.post(COURIER_URL, json=courier_data)

    @staticmethod
    @allure.step("Авторизация курьера")
    def login_courier(credentials: dict) -> requests.Response:
        return requests.post(COURIER_LOGIN_URL, json=credentials)

    @staticmethod
    @allure.step("Удаление курьера")
    def delete_courier(courier_id: int) -> requests.Response:
        return requests.delete(f"{COURIER_URL}/{courier_id}")


class OrdersAPI:
    @staticmethod
    @allure.step("Создание заказа")
    def create_order(order_data: dict) -> requests.Response:
        return requests.post(ORDERS_URL, json=order_data)

    @staticmethod
    @allure.step("Получение списка заказов")
    def get_orders() -> requests.Response:
        return requests.get(ORDERS_URL)

    @staticmethod
    @allure.step("Отмена заказа")
    def cancel_order(track: int) -> requests.Response:
        return requests.put(ORDERS_CANCEL_URL, json={"track": track})
