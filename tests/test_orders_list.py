import requests
from configuration import BASE_URL

class TestOrdersList:
    def test_get_orders_list(self):
        response = requests.get(f'{BASE_URL}/api/v1/orders')
        assert response.status_code == 200
        assert isinstance(response.json()['orders'], list)