import allure
import requests
import random
import string
from configuration import BASE_URL

@allure.step("Генерация случайной строки длиной {length}")
def generate_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

@allure.step("Регистрация нового курьера")
def register_new_courier():
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)
    
    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }
    
    with allure.step(f"Отправка запроса на регистрацию курьера {login}"):
        response = requests.post(f'{BASE_URL}/api/v1/courier', data=payload)
    
    if response.status_code == 201:
        allure.attach(f"Регистрация успешна. Логин: {login}, Имя: {first_name}", 
                     name="Данные курьера")
        return payload
    else:
        error_message = f"Ошибка регистрации: {response.status_code} - {response.text}"
        allure.attach(error_message, name="Ошибка регистрации")
        raise Exception(error_message)

@allure.step("Авторизация курьера {login}")
def login_courier(login, password):
    payload = {
        "login": login,
        "password": password
    }
    
    with allure.step("Отправка запроса на авторизацию"):
        response = requests.post(f'{BASE_URL}/api/v1/courier/login', data=payload)
    
    allure.attach(f"Статус ответа: {response.status_code}", name="Результат авторизации")
    return response

@allure.step("Удаление курьера {login}")
def delete_courier(login, password):
    try:
        with allure.step("Получение ID курьера для удаления"):
            login_response = login_courier(login, password)
        
        if login_response.status_code == 200:
            courier_id = login_response.json()['id']
            with allure.step(f"Отправка запроса на удаление курьера ID {courier_id}"):
                response = requests.delete(f'{BASE_URL}/api/v1/courier/{courier_id}')
            
            allure.attach(f"Статус удаления: {response.status_code}", name="Результат удаления")
            return response
        else:
            error_message = f"Не удалось авторизоваться для удаления: {login_response.status_code}"
            allure.attach(error_message, name="Ошибка удаления")
            return login_response
            
    except requests.exceptions.RequestException as e:
        # Обработка ошибок сетевого запроса
        error_message = f"Сетевая ошибка при удалении курьера: {str(e)}"
        allure.attach(error_message, name="Сетевая ошибка")
        raise Exception(error_message) from e
        
    except (ValueError, KeyError) as e:
        # Обработка ошибок парсинга JSON
        error_message = f"Ошибка обработки ответа сервера: {str(e)}"
        allure.attach(error_message, name="Ошибка обработки данных")
        raise Exception(error_message) from e