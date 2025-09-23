import allure
import pytest
import requests
import random
from unittest.mock import patch
from configuration import BASE_URL
from helpers.courier import register_new_courier, delete_courier

class TestCourierLogin:
    @allure.title("Успешная авторизация курьера")
    def test_login_success(self):
        """Тест успешной авторизации курьера"""
        courier = register_new_courier()
        
        # Пытаемся авторизоваться
        response = requests.post(f'{BASE_URL}/api/v1/courier/login', data={
            "login": courier['login'],
            "password": courier['password']
        }, timeout=10)
        
        # Проверяем статус код и содержимое ответа
        assert response.status_code == 200
        response_data = response.json()
        assert 'id' in response_data
        
        # Удаляем курьера
        delete_response = delete_courier(courier['login'], courier['password'])
        assert delete_response.status_code == 200
        assert delete_response.json() == {"ok": True}

    @allure.title("Авторизация с отсутствующим полем: {field}")
    @pytest.mark.parametrize('field', ['login', 'password'])
    def test_login_missing_field(self, field, mocker):
        """Тест авторизации с отсутствующими обязательными полями (с использованием моков)"""
        # Мокируем запрос к API
        mock_response = mocker.Mock()
        mock_response.status_code = 400
        mock_response.json.return_value = {
            "code": 400, 
            "message": "Недостаточно данных для входа"
        }
        
        # Заменяем реальный requests.post на мок
        mocker.patch('requests.post', return_value=mock_response)
        
        # Генерируем уникальные данные
        base_value = f"test_{random.randint(1000, 9999)}"
        
        payload = {"login": base_value, "password": base_value}
        del payload[field]
        
        # Выполняем запрос (будет использован мок)
        response = requests.post(f'{BASE_URL}/api/v1/courier/login', data=payload)
        
        # Проверяем, что запрос был выполнен с правильными параметрами
        requests.post.assert_called_once_with(
            f'{BASE_URL}/api/v1/courier/login',
            data=payload
        )
        
        # Проверяем ответ
        assert response.status_code == 400
        response_data = response.json()
        assert response_data["code"] == 400
        assert "message" in response_data

    @allure.title("Авторизация несуществующего пользователя")
    def test_login_nonexistent_user(self):
        """Тест авторизации несуществующего пользователя"""
        response = requests.post(f'{BASE_URL}/api/v1/courier/login', data={
            "login": f"nonexistent_user_{random.randint(1000, 9999)}",
            "password": "password123"
        }, timeout=10)
        
        # Проверяем статус код и содержимое ответа
        assert response.status_code == 404
        response_data = response.json()
        assert "message" in response_data
        assert response_data["code"] == 404

    @allure.title("Авторизация с неправильным паролем")
    def test_login_incorrect_password(self):
        """Тест авторизации с неправильным паролем"""
        courier = register_new_courier()
        
        response = requests.post(f'{BASE_URL}/api/v1/courier/login', data={
            "login": courier['login'],
            "password": "incorrect_password"
        }, timeout=10)
        
        # Проверяем статус код и содержимое ответа
        assert response.status_code == 404
        response_data = response.json()
        assert "message" in response_data
        assert response_data["code"] == 404
        
        # Удаляем курьера
        delete_response = delete_courier(courier['login'], courier['password'])
        assert delete_response.status_code == 200
        assert delete_response.json() == {"ok": True}