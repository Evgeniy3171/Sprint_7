import allure
import pytest
import requests
from configuration import BASE_URL
from helpers.courier import login_courier
from helpers.order import get_order_by_track

class TestAdditional:
    @allure.title("Успешное удаление курьера")
    def test_delete_courier_success(self, create_and_delete_courier):
        """Тест успешного удаления курьера с использованием фикстуры"""
        courier = create_and_delete_courier
        login_response = login_courier(courier['login'], courier['password'])
        courier_id = login_response.json()['id']
        
        response = requests.delete(f'{BASE_URL}/api/v1/courier/{courier_id}')
        
        # Проверяем статус код и содержимое ответа
        assert response.status_code == 200
        assert response.json() == {"ok": True}

    @allure.title("Успешное принятие заказа курьером")
    def test_accept_order_success(self, create_and_delete_courier, create_and_cancel_order):
        """Тест успешного принятия заказа с использованием фикстур"""
        courier = create_and_delete_courier
        order_data = create_and_cancel_order
        
        # Логинимся курьером
        login_response = login_courier(courier['login'], courier['password'])
        courier_id = login_response.json()['id']
        
        # Получаем ID заказа по его track number
        order_info_response = get_order_by_track(order_data['track'])
        order_id = order_info_response.json()['order']['id']
        
        # Принимаем заказ
        response = requests.put(
            f'{BASE_URL}/api/v1/orders/accept/{order_id}',
            params={"courierId": courier_id}
        )
        
        # Проверяем статус код и содержимое ответа
        assert response.status_code == 200
        assert response.json() == {"ok": True}

    @allure.title("Получение заказа по номеру трека")
    def test_get_order_by_track_success(self, create_and_cancel_order):
        """Тест успешного получения заказа по треку с использованием фикстуры"""
        order_data = create_and_cancel_order
        
        # Получаем заказ по track number
        response = get_order_by_track(order_data['track'])
        
        # Проверяем статус код и содержимое ответа
        assert response.status_code == 200
        response_data = response.json()
        assert 'order' in response_data
        # Дополнительные проверки содержимого заказа
        order = response_data['order']
        assert 'id' in order
        assert 'track' in order
        assert 'status' in order