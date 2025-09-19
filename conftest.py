import pytest
from helpers.courier import register_new_courier, delete_courier
from helpers.order import create_order, cancel_order

@pytest.fixture
def create_and_delete_courier():
    """Фикстура для создания и последующего удаления курьера"""
    courier = register_new_courier()
    yield courier
    # Финализатор - будет выполнен даже при падении теста
    delete_response = delete_courier(courier['login'], courier['password'])
    # Проверяем, что удаление прошло успешно или курьер уже удален/не найден
    assert delete_response.status_code in [200, 404, 409]

@pytest.fixture
def create_and_cancel_order():
    """Фикстура для создания и последующей отмены заказа"""
    order_response = create_order()
    order_data = order_response.json()
    yield order_data
    # Финализатор - будет выполнен даже при падении теста
    if 'track' in order_data:
        cancel_response = cancel_order(order_data['track'])
        # Проверяем, что отмена прошла успешно или заказ уже отменен/не может быть отменен
        assert cancel_response.status_code in [200, 404, 409]