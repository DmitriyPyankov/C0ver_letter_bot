import requests
import json

# Замените следующие значения на ваши реальные данные
client_id = "ваш_client_id"
redirect_uri = "ваш_redirect_uri"
state = 121

# Формирование URL для перенаправления пользователя
authorize_url = f"https://hh.ru/oauth/authorize?response_type=code&client_id={client_id}&state={state}&redirect_uri={redirect_uri}"

# Открываем URL в браузере и пользователь авторизуется

# Замените этот код на код, который будет использован в вашем приложении для получения кода авторизации
authorization_code = "ваш_код_авторизации"

# Замените настоящие данные авторизации
client_secret = "ваш_client_secret"

# Запрос на получение токена
token_url = "https://hh.ru/oauth/token"
data = {
    "grant_type": "authorization_code",
    "client_id": client_id,
    "client_secret": client_secret,
    "code": authorization_code,
    "redirect_uri": redirect_uri,
}

response = requests.post(token_url, data=data)
token_data = response.json()

# В этой переменной будет содержаться ваш access token
access_token = token_data.get("access_token")
print("Access Token:", access_token)