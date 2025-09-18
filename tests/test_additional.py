import pytest
import requests
import random
from configuration import BASE_URL
from helpers.courier import register_new_courier, delete_courier, login_courier
from helpers.order import create_order, cancel_order, get_order_by_track

class TestAdditional:
    def test_delete_courier_success(self):
        courier = register_new_courier()
        login_response = login_courier(courier['login'], courier['password'])
        courier_id = login_response.json()['id']
        
        response = requests.delete(f'{BASE_URL}/api/v1/courier/{courier_id}')
        assert response.status_code == 200
        assert response.json() == {"ok": True}

    def test_accept_order_success(self):
        # Создадим курьера
        courier = register_new_courier()
        login_response = login_courier(courier['login'], courier['password'])
        courier_id = login_response.json()['id']
        
        # Создадим заказ
        order_response = create_order()
        order_track = order_response.json()['track']
        
        # Получим ID заказа по его track number
        order_info_response = get_order_by_track(order_track)
        order_id = order_info_response.json()['order']['id']
        
        # Принимаем заказ
        response = requests.put(
            f'{BASE_URL}/api/v1/orders/accept/{order_id}',
            params={"courierId": courier_id}
        )
        assert response.status_code == 200
        assert response.json() == {"ok": True}
        
        # Отменяем заказ и удаляем курьера
        cancel_order(order_track)
        delete_courier(courier['login'], courier['password'])

    def test_get_order_by_track_success(self):
        # Создадим заказ
        order_response = create_order()
        order_track = order_response.json()['track']
        
        # Получаем заказ по track number
        response = get_order_by_track(order_track)
        assert response.status_code == 200
        assert 'order' in response.json()
        
        # Отменяем заказ
        cancel_order(order_track)