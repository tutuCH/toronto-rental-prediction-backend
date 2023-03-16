import requests

BASE = "http://127.0.0.1:5000/"

response = requests.get(BASE + 'get-rental-prediction-price')
print(response.json())