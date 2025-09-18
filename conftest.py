import pytest
import requests
from helpers.courier import register_new_courier, delete_courier
from helpers.order import create_order, cancel_order

@pytest.fixture
def create_and_delete_courier():
    courier = register_new_courier()
    yield courier
    delete_courier(courier['login'], courier['password'])

@pytest.fixture
def create_and_cancel_order():
    order_response = create_order()
    order_data = order_response.json()
    yield order_data
    if 'track' in order_data:
        cancel_order(order_data['track'])