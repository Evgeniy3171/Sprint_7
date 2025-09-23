import allure
import random
import requests
from configuration import BASE_URL

def create_order(color=None):
    color_description = "без цвета" if not color else str(color)
    with allure.step(f"Создание заказа с цветом: {color_description}"):
        # Генерируем уникальные данные для заказа
        random_suffix = random.randint(1000, 9999)
        
        payload = {
            "firstName": f"Тест_{random_suffix}",
            "lastName": f"Тестов_{random_suffix}",
            "address": f"ул. Тестовая, {random_suffix}",
            "metroStation": random.randint(1, 10),
            "phone": f"+7999{random.randint(1000000, 9999999)}",
            "rentTime": random.randint(1, 7),
            "deliveryDate": "2024-09-17",
            "comment": f"Тестовый заказ {random_suffix}"
        }
        
        if color:
            payload["color"] = color
        
        with allure.step("Отправка запроса на создание заказа"):
            response = requests.post(f'{BASE_URL}/api/v1/orders', json=payload)
        
        allure.attach(f"Статус ответа: {response.status_code}", name="Результат создания заказа")
        if response.status_code == 201:
            track_number = response.json().get('track')
            allure.attach(f"Номер трека заказа: {track_number}", name="Трек заказа")
        
        return response

@allure.step("Отмена заказа с треком {order_id}")
def cancel_order(order_id):
    with allure.step("Отправка запроса на отмену заказа"):
        response = requests.put(f'{BASE_URL}/api/v1/orders/cancel', params={"track": order_id})
    
    allure.attach(f"Статус отмены: {response.status_code}", name="Результат отмены заказа")
    return response

@allure.step("Получение заказа по треку {track_id}")
def get_order_by_track(track_id):
    with allure.step("Отправка запроса на получение заказа по треку"):
        response = requests.get(f'{BASE_URL}/api/v1/orders/track', params={"t": track_id})
    
    allure.attach(f"Статус ответа: {response.status_code}", name="Результат получения заказа")
    return response