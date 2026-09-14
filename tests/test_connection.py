import requests

def test_connection():
    response = requests.get('https://restful-booker.herokuapp.com/booking')
    assert response.status_code == 200