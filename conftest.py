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