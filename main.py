import os

import requests

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_URL = "https://api.telegram.org/bot"

response = requests.get(f"{API_URL}{BOT_TOKEN}/getMe")

if response.status_code == 200:
    print(response.json())
else:
    print(f"Ошибка запроса: {response.status_code}, {response.text}")
