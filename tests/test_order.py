import allure
import pytest
from helpers.order import create_order

class TestOrderCreation:
    @allure.title("Создание заказа с цветом: {color}")
    @pytest.mark.parametrize('color', [['BLACK'], ['GREY'], ['BLACK', 'GREY'], []])
    def test_create_order_with_different_colors(self, color, create_and_cancel_order_with_color):
        """Тест создания заказа с разными цветами с использованием фикстуры"""
        create_order_func, register_cleanup = create_and_cancel_order_with_color
        
        # Создаем заказ с указанным цветом через фикстуру
        order_data, response = create_order_func(color)
        
        # Проверяем, что заказ создан успешно и содержит track
        assert response.status_code == 201
        assert 'track' in order_data, "Ответ должен содержать поле 'track'"
        
        # Регистрируем заказ для отмены в фикстуре
        track_number = order_data['track']
        register_cleanup(track_number)
        
        # Дополнительные проверки
        assert isinstance(track_number, int), "Track number должен быть целым числом"
        assert track_number > 0, "Track number должен быть положительным числом"
        
        # Фикстура автоматически отменит заказ после теста