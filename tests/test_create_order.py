import allure
import pytest

from data.test_data import OrderData
from helpers.api_helpers import OrdersAPI

@allure.epic("Заказы")
@allure.feature("Создание заказа")
class TestCreateOrder:

    @allure.title("Создание заказа")
    @pytest.mark.parametrize("test_case", [
        pytest.param({"color": ["BLACK"]}, id="black_color"),
        pytest.param({"color": ["GREY"]}, id="grey_color"),
        pytest.param({"color": ["BLACK", "GREY"]}, id="both_colors"),
        pytest.param({"color": []}, id="no_color"),
        pytest.param({}, id="without_color_field")
    ])
    def test_create_order(self, test_case, cleanup_orders, save_track):
        order_data = OrderData.BASE_ORDER
        order_data.update(test_case)

        with allure.step(f"Создание заказа с параметрами {test_case}"):
            response = OrdersAPI.create_order(order_data)

        with allure.step("Проверка ответа"):
            assert response.status_code == 201, f"Неожиданный код ответа: {response.status_code}"
            response_data = response.json()
            assert "track" in response_data, "В ответе отсутствует поле track"
            track = save_track(response)
            assert isinstance(track, int), f"Track не является целым числом: {track}"
            assert track > 0, f"Track должен быть положительным числом, получено: {track}"
