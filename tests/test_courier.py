import allure
import pytest
import requests
from configuration import BASE_URL
from helpers.courier import register_new_courier, delete_courier, generate_random_string

class TestCourierCreation:
    @allure.title("Создание курьера без обязательных полей: {missing_field}")
    @pytest.mark.parametrize('missing_field', ['login', 'password'])
    def test_create_courier_missing_login_or_password(self, missing_field):
        """Тест создания курьера без обязательных полей login или password"""
        # Генерируем уникальные данные для каждого теста
        login = f"test_login_{generate_random_string(5)}"
        password = f"test_pass_{generate_random_string(5)}"
        first_name = f"test_name_{generate_random_string(5)}"
        
        courier_data = {
            "login": login,
            "password": password,
            "firstName": first_name
        }
        del courier_data[missing_field]
        
        response = requests.post(f'{BASE_URL}/api/v1/courier', data=courier_data)
        
        # Проверяем статус код и содержимое ответа
        assert response.status_code == 400
        response_data = response.json()
        assert "message" in response_data
        assert "code" in response_data

    @allure.title("Создание курьера без поля firstName")
    def test_create_courier_missing_first_name(self):
        """Тест создания курьера без поля firstName"""
        # Генерируем уникальные данные
        login = f"test_login_{generate_random_string(5)}"
        password = f"test_pass_{generate_random_string(5)}"
        
        courier_data = {
            "login": login,
            "password": password
            # Поле firstName отсутствует
        }
        
        response = requests.post(f'{BASE_URL}/api/v1/courier', data=courier_data)
        
        # Сервер не требует firstName, поэтому проверяем успешное создание
        assert response.status_code == 201
        response_data = response.json()
        assert response_data == {"ok": True}
        
        # Удаляем созданного курьера
        delete_response = delete_courier(login, password)
        assert delete_response.status_code == 200
        assert delete_response.json() == {"ok": True}

    @allure.title("Создание дубликата курьера")
    def test_create_duplicate_courier(self, create_and_delete_courier):
        """Тест создания дубликата курьера"""
        response = requests.post(f'{BASE_URL}/api/v1/courier', data=create_and_delete_courier)
        
        # Проверяем статус код и содержимое ответа
        assert response.status_code == 409
        response_data = response.json()
        assert "message" in response_data
        assert response_data["code"] == 409

    @allure.title("Успешное создание курьера")
    def test_create_courier_success(self):
        """Тест успешного создания курьера"""
        courier_data = register_new_courier()
        assert 'login' in courier_data
        assert 'password' in courier_data
        assert 'firstName' in courier_data
        
        # Удаляем созданного курьера и проверяем ответ
        delete_response = delete_courier(courier_data['login'], courier_data['password'])
        assert delete_response.status_code == 200
        assert delete_response.json() == {"ok": True}