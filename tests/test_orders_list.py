import allure
import requests
from configuration import BASE_URL

class TestOrdersList:
    @allure.title("Получение списка заказов")
    def test_get_orders_list(self):
        """Тест получения списка заказов"""
        response = requests.get(f'{BASE_URL}/api/v1/orders')
        
        # Проверяем статус код и содержимое ответа
        assert response.status_code == 200
        response_data = response.json()
        assert isinstance(response_data['orders'], list)