import requests
import random
import string
from configuration import BASE_URL

def generate_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

def register_new_courier():
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)
    
    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }
    
    response = requests.post(f'{BASE_URL}/api/v1/courier', data=payload)
    
    if response.status_code == 201:
        return payload
    else:
        raise Exception(f"Failed to create courier: {response.text}")

def login_courier(login, password):
    payload = {
        "login": login,
        "password": password
    }
    
    response = requests.post(f'{BASE_URL}/api/v1/courier/login', data=payload)
    return response

def delete_courier(login, password):
    try:
        login_response = login_courier(login, password)
        
        if login_response.status_code == 200:
            courier_id = login_response.json()['id']
            response = requests.delete(f'{BASE_URL}/api/v1/courier/{courier_id}')
            return response
        else:
            return login_response
    except Exception as e:
        print(f"Error deleting courier: {e}")
        return None