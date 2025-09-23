import pytest
import allure
from helpers.courier import register_new_courier, delete_courier
from helpers.order import create_order, cancel_order

@pytest.fixture
def create_and_delete_courier():
    """Фикстура для создания и последующего удаления курьера"""
    courier = register_new_courier()
    yield courier
    # Финализатор - будет выполнен даже при падении теста
    try:
        delete_courier(courier['login'], courier['password'])
    except Exception as e:
        allure.attach(f"Ошибка при удалении курьера: {str(e)}", name="Предупреждение")

@pytest.fixture
def create_and_cancel_order():
    """Фикстура для создания и последующей отмены заказа"""
    response = create_order()
    order_data = response.json()
    yield order_data
    # Финализатор - будет выполнен даже при падении теста
    try:
        if 'track' in order_data:
            cancel_order(order_data['track'])
    except Exception as e:
        allure.attach(f"Ошибка при отмене заказа: {str(e)}", name="Предупреждение")

@pytest.fixture
def create_and_cancel_order_with_color():
    """Фикстура для создания заказа с цветом и последующей отмены"""
    def _create_order(color=None):
        response = create_order(color)
        order_data = response.json()
        return order_data, response
    
    orders_to_cancel = []
    
    def _register_for_cleanup(track_number):
        orders_to_cancel.append(track_number)
    
    yield _create_order, _register_for_cleanup
    
    # Финализатор - отменяет все зарегистрированные заказы
    for track_number in orders_to_cancel:
        try:
            if track_number:
                cancel_order(track_number)
        except Exception as e:
            allure.attach(f"Ошибка при отмене заказа {track_number}: {str(e)}", name="Предупреждение")