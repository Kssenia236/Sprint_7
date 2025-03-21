import allure
import pytest

from data.response_messages import CourierMessages
from helpers.api_helpers import CourierAPI


@allure.epic("Курьеры")
@allure.feature("Создание курьера")
class TestCreateCourier:

    @allure.title("Проверка создания курьера")
    @pytest.mark.parametrize("test_case", [
        pytest.param(
            {
                "case": "valid",
                "data_mod": lambda x: x,
                "expected_status": 201,
                "expected_response": {"ok": True},
                "description": "валидные данные"
            },
            id="create_valid_courier"
        ),
        pytest.param(
            {
                "case": "duplicate",
                "data_mod": lambda x: x,
                "expected_status": 409,
                "expected_response": {
                    "code": 409,
                    "message": CourierMessages.DUPLICATE_LOGIN
                },
                "description": "дубликат курьера"
            },
            id="create_duplicate_courier"
        ),
        pytest.param(
            {
                "case": "no_login",
                "data_mod": lambda x: {k: v for k, v in x.items() if k != "login"},
                "expected_status": 400,
                "expected_response": {
                    "code": 400,
                    "message": CourierMessages.MISSING_REQUIRED_FIELDS
                },
                "description": "без логина"
            },
            id="missing_login"
        ),
        pytest.param(
            {
                "case": "no_password",
                "data_mod": lambda x: {k: v for k, v in x.items() if k != "password"},
                "expected_status": 400,
                "expected_response": {
                    "code": 400,
                    "message": CourierMessages.MISSING_REQUIRED_FIELDS
                },
                "description": "без пароля"
            },
            id="missing_password"
        ),
        pytest.param(
            {
                "case": "no_firstname",
                "data_mod": lambda x: {k: v for k, v in x.items() if k != "firstName"},
                "expected_status": 201,
                "expected_response": {"ok": True},
                "description": "без имени (необязательное поле)"
            },
            id="missing_firstname"
        ),
        pytest.param(
            {
                "case": "existing_login",
                "data_mod": lambda x: {"login": x["login"], "password": "new_pass", "firstName": "new_name"},
                "expected_status": 409,
                "expected_response": {
                    "code": 409,
                    "message": CourierMessages.DUPLICATE_LOGIN
                },
                "description": "существующий логин"
            },
            id="existing_login"
        )
    ])
    def test_create_courier(self, test_case, new_courier_data):
        with allure.step(f"Подготовка данных для теста: {test_case['description']}"):
            courier_data = new_courier_data
            if test_case["case"] in ["duplicate", "existing_login"]:
                first_response = CourierAPI.create_courier(courier_data)
                assert first_response.status_code == 201, "Не удалось создать первого курьера"
            test_data = test_case["data_mod"](courier_data)
        with allure.step(f"Создание курьера: {test_case['description']}"):
            response = CourierAPI.create_courier(test_data)
        with allure.step("Проверка ответа"):
            assert response.status_code == test_case[
                "expected_status"], f"Неожиданный код ответа: {response.status_code}"
            response_data = response.json()
            assert response_data == test_case["expected_response"], f"Неожиданное тело ответа: {response_data}"
