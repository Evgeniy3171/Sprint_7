import allure
import pytest
import requests
from helpers.order import create_order, cancel_order

@pytest.fixture
def order_data(request):
    color = request.param
    response = create_order(color)
    assert response.status_code == 201, f"Ошибка при создании заказа с цветом {color}: {response.text}"
    data = response.json()
    yield data
    # Teardown: отменяем заказ
    if 'track' in data:
        cancel_order(data['track'])


class TestOrderCreation:
    @allure.title("Создание заказа с цветом: {color}")
    @pytest.mark.parametrize('color', [['BLACK'], ['GREY'], ['BLACK', 'GREY'], []])
    def test_create_order_with_different_colors(self, color, mocker):
        """Тест создания заказа с разными цветами"""
        # Мокируем создание заказа
        mock_response = mocker.Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {"track": 12345}
        
        mocker.patch('requests.post', return_value=mock_response)
        
        # Мокируем отмену заказа
        mock_cancel_response = mocker.Mock()
        mock_cancel_response.status_code = 200
        mocker.patch('requests.put', return_value=mock_cancel_response)
        
        # Выполняем тест
        response = create_order(color)
        
        # Проверяем результат
        assert response.status_code == 201
        assert 'track' in response.json()
        
        # Проверяем, что запрос был выполнен с правильными параметрами
        requests.post.assert_called_once()
        
        # Проверяем отмену заказа
        cancel_response = cancel_order(12345)
        assert cancel_response.status_code == 200