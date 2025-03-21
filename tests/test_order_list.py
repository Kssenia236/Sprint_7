import allure
from helpers.api_helpers import OrdersAPI


@allure.epic("Orders API")
class TestOrderList:
    @allure.title("Проверка получения списка заказов")
    def test_get_orders_returns_orders_list(self, test_order_data, create_test_order, save_track):
        response = OrdersAPI.get_orders()
        assert response.status_code == 200
        assert isinstance(response.json()["orders"], list)

    @allure.title("Проверка структуры заказа в списке")
    def test_order_contains_required_fields(self, test_order_data, create_test_order, save_track):
        response = OrdersAPI.get_orders()
        orders = response.json()["orders"]
        required_fields = ["id", "firstName", "lastName", "address", "metroStation",
                           "phone", "rentTime", "status"]

        for order in orders:
            for field in required_fields:
                assert field in order, f"Поле {field} отсутствует в заказе"