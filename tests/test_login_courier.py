import allure
import pytest

from data.response_messages import CourierLoginMessages
from helpers.api_helpers import CourierAPI


@allure.epic("Курьеры")
@allure.feature("Логин курьера")
class TestLoginCourier:

    @allure.title("Проверка логина курьера с разными наборами данных")
    @pytest.mark.parametrize("test_case", [
        pytest.param(
            {
                "data_modifier": lambda x: {
                    "login": x["login"],
                    "password": x["password"]
                },
                "expected_status": 200,
                "check_id": True,
                "create_courier": True,
                "description": "валидные данные"
            },
            id="valid_login"
        ),
        pytest.param(
            {
                "data_modifier": lambda x: {
                    "login": "incorrect_" + x["login"],
                    "password": x["password"]
                },
                "expected_status": 404,
                "expected_response": {
                    "code": 404,
                    "message": CourierLoginMessages.ACCOUNT_NOT_FOUND
                },
                "create_courier": True,
                "description": "неверный логин"
            },
            id="wrong_login"
        ),
        pytest.param(
            {
                "data_modifier": lambda x: {
                    "login": x["login"],
                    "password": "incorrect_" + x["password"]
                },
                "expected_status": 404,
                "expected_response": {
                    "code": 404,
                    "message": CourierLoginMessages.ACCOUNT_NOT_FOUND
                },
                "create_courier": True,
                "description": "неверный пароль"
            },
            id="wrong_password"
        ),
        pytest.param(
            {
                "data_modifier": lambda x: {
                    "password": x["password"]
                },
                "expected_status": 400,
                "expected_response": {
                    "code": 400,
                    "message": CourierLoginMessages.INSUFFICIENT_DATA
                },
                "create_courier": True,
                "description": "без логина"
            },
            id="missing_login"
        )
    ])
    def test_login_courier(self, new_courier_data, test_case):
        courier_data = new_courier_data.copy()
        courier_id = None
        with allure.step(f"Подготовка тестовых данных: {test_case['description']}"):
            if test_case.get("create_courier"):
                create_response = CourierAPI.create_courier(courier_data)
                assert create_response.status_code == 201
            login_data = test_case["data_modifier"](courier_data)
        with allure.step(f"Попытка входа: {test_case['description']}"):
            login_response = CourierAPI.login_courier(login_data)
            response_data = login_response.json()
        with allure.step("Проверка ответа"):
            assert login_response.status_code == test_case["expected_status"]
            if test_case.get("check_id"):
                assert "id" in response_data
                assert isinstance(response_data["id"], int)
                courier_id = response_data["id"]
            elif "expected_response" in test_case:
                assert response_data == test_case["expected_response"]
        if courier_id:
            with allure.step("Удаление тестового курьера"):
                CourierAPI.delete_courier(courier_id)

    @allure.title("Проверка логина несуществующего курьера")
    def test_login_non_existent_courier(self, new_courier_data):
        with allure.step("Попытка входа с данными несуществующего курьера"):
            login_data = {
                "login": new_courier_data["login"],
                "password": new_courier_data["password"]
            }
            response = CourierAPI.login_courier(login_data)
            response_data = response.json()
            assert response.status_code == 404
            assert response_data == {
                "code": 404,
                "message": CourierLoginMessages.ACCOUNT_NOT_FOUND
            }
