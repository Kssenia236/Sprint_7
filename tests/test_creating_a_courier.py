import allure
import requests
import random
import string
from courier_helper import generate_courier_data

def register_new_courier_and_return_login_password():
    def generate_random_string(length):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for _ in range(length))

    login_pass = []
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier', data=payload)

    if response.status_code == 201:
        login_pass.append(login)
        login_pass.append(password)
        login_pass.append(first_name)

    return login_pass


class TestCreateCourier:
    @allure.step("Тест на создание курьера")
    def test_create_courier(self, create_courier, courier_data):
        response = create_courier(courier_data)
        assert response.status_code == 201

    @allure.step("Тест на невозможность создания дублирующего курьера")
    def test_cannot_create_duplicate_courier(self, create_courier, courier_data):
        response = create_courier(courier_data)
        assert response.status_code == 201

        response = create_courier(courier_data)
        assert response.status_code == 409

    @allure.step("Тест на создание курьера без обязательных полей")
    def test_create_courier_without_required_fields(self, create_courier, courier_data):
        data = courier_data.copy()
        del data['password']
        response = create_courier(data)
        assert response.status_code == 400

    @allure.step("Тест на корректный ответ при создании курьера")
    def test_create_courier_returns_correct_response(self, create_courier, courier_data):
        response = create_courier(courier_data)
        assert response.status_code == 201
        assert response.json() == {"ok": True}

    @allure.step("Тест на ошибки при отсутствии обязательных полей")
    def test_create_courier_missing_required_fields_returns_error(self, create_courier, courier_data):
        data_without_login = courier_data.copy()
        del data_without_login['login']
        with allure.step("Удаляем поле 'login' из данных курьера"):
            response = create_courier(data_without_login)
        assert response.status_code == 400
        assert response.json()["message"] == "Недостаточно данных для создания учетной записи"

        data_without_password = courier_data.copy()
        del data_without_password['password']
        with allure.step("Удаляем поле 'password' из данных курьера"):
            response = create_courier(data_without_password)
        assert response.status_code == 400
        assert response.json()["message"] == "Недостаточно данных для создания учетной записи"

    @allure.step("Тест на создание курьера с уже существующим логином")
    def test_create_courier_with_existing_login(self, create_courier, courier_data):
        response = create_courier(courier_data)
        assert response.status_code == 201
        assert response.json()['ok'] == True

        duplicate_courier_data = generate_courier_data()
        duplicate_courier_data['login'] = courier_data['login']
        with allure.step("Создаем данные для дублирующего курьера с существующим логином"):
            response = create_courier(duplicate_courier_data)
        assert response.status_code == 409
        assert response.json()['message'] == "Этот логин уже используется. Попробуйте другой."
