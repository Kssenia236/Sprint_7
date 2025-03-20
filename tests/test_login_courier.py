import allure
import pytest
import requests


class TestLoginCourier:
    @allure.title("Проверка успешной авторизации курьера")
    def test_courier_can_login(self, base_url, courier_data):
        with allure.step("Создание курьера"):
            create_response = requests.post(f"{base_url}", json=courier_data)
            assert create_response.status_code == 201

        with allure.step("Авторизация курьера"):
            login_data = {'login': courier_data['login'], 'password': courier_data['password']}
            response = requests.post(f'{base_url}/login', json=login_data)
            assert response.status_code == 200
            assert 'id' in response.json()

    @allure.title("Проверка авторизации курьера с обязательными полями")
    def test_courier_login_required_fields(self, base_url, courier_data):
        with allure.step("Создание курьера"):
            create_response = requests.post(f"{base_url}", json=courier_data)
            assert create_response.status_code == 201

        with allure.step("Авторизация с обязательными полями"):
            login_data = {"login": courier_data["login"], "password": courier_data["password"]}
            response = requests.post(f"{base_url}/login", json=login_data)
            assert response.status_code == 200
            assert "id" in response.json()

    @allure.title("Проверка авторизации курьера с неверными данными")
    def test_courier_login_invalid_data(self, base_url, courier_data, create_courier):
        with allure.step("Создание тестового курьера"):
            create_courier(courier_data)

        test_cases = [
            {
                "login": "incorrect_" + courier_data["login"],
                "password": courier_data["password"],
                "expected_status": 404,
                "expected_message": "Учетная запись не найдена"
            },
            {
                "login": courier_data["login"],
                "password": "incorrect_" + courier_data["password"],
                "expected_status": 404,
                "expected_message": "Учетная запись не найдена"
            }
        ]

        for case in test_cases:
            with allure.step(f"Проверка с логином '{case['login']}' и паролем '{case['password']}'"):
                response = requests.post(f"{base_url}/login",
                                         json={"login": case["login"], "password": case["password"]})
                assert response.status_code == case["expected_status"]
                assert response.json()["message"] == case["expected_message"]

    @allure.title("Проверка авторизации курьера с отсутствующими обязательными полями")
    @pytest.mark.parametrize("request_data",
                             [{"login": "", "password": "test_password"},
                              {"password": "test_password"}])
    def test_courier_login_missing_required_fields(self, base_url, request_data):
        with allure.step(f"Попытка входа с данными: {request_data}"):
            response = requests.post(f"{base_url}/login", json=request_data)
            assert response.status_code == 400
            assert response.json()["message"] == "Недостаточно данных для входа"

    @allure.title("Проверка авторизации несуществующего курьера")
    def test_login_non_existent_courier(self, base_url, courier_data):
        with allure.step("Попытка входа с данными несуществующего курьера"):
            response = requests.post(f"{base_url}/login",
                                     json={"login": courier_data["login"],
                                           "password": courier_data["password"]})
            assert response.status_code == 404
            assert response.json()["message"] == "Учетная запись не найдена"

    @allure.title("Проверка успешной авторизации курьера и получения id")
    def test_successful_login_returns_id(self, base_url, courier_data):
        with allure.step("Создание тестового курьера"):
            create_response = requests.post(f"{base_url}", json=courier_data)
            assert create_response.status_code == 201

        with allure.step("Авторизация курьера"):
            login_response = requests.post(f"{base_url}/login",
                                           json={"login": courier_data["login"],
                                                 "password": courier_data["password"]})
            assert login_response.status_code == 200
            response_data = login_response.json()
            assert "id" in response_data