import allure
import requests


class TestOrderList:
    @allure.title("Проверка получения списка заказов")
    def test_get_orders_returns_orders_list(self, orders_url, test_order_data, create_test_order, cleanup_order):
        with allure.step("Создание тестового заказа"):
            create_response = create_test_order(test_order_data)
            assert create_response.status_code == 201
            # Сохраняем track номер для последующей очистки
            track = create_response.json().get("track")
            if track:
                cleanup_order.append(track)

        with allure.step("Получение списка заказов"):
            response = requests.get(orders_url)
            assert response.status_code == 200, "Неверный код ответа"

        with allure.step("Проверка структуры ответа"):
            response_data = response.json()
            assert "orders" in response_data, "В ответе отсутствует поле 'orders'"
            assert isinstance(response_data["orders"], list), "Поле 'orders' не является списком"
            assert len(response_data["orders"]) > 0, "Список заказов пуст"

        with allure.step("Проверка структуры заказа"):
            first_order = response_data["orders"][0]
            expected_fields = [
                "id", "firstName", "lastName", "address",
                "metroStation", "phone", "rentTime", "deliveryDate",
                "track", "status", "createdAt", "updatedAt"
            ]
            for field in expected_fields:
                assert field in first_order, f"В заказе отсутствует поле '{field}'"