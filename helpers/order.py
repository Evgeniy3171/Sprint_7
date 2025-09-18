import random
import requests
from configuration import BASE_URL

def create_order(color=None):
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
    
    response = requests.post(f'{BASE_URL}/api/v1/orders', json=payload)
    return response

def cancel_order(order_id):
    response = requests.put(f'{BASE_URL}/api/v1/orders/cancel', params={"track": order_id})
    return response

def get_order_by_track(track_id):
    response = requests.get(f'{BASE_URL}/api/v1/orders/track', params={"t": track_id})
    return response