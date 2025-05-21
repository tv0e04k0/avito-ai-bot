import requests

def get_avito_token(client_id, client_secret):
    url = "https://api.avito.ru/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret
    }
    response = requests.post(url, headers=headers, data=data)

    # Выводим ответ полностью в лог, чтобы увидеть ошибку
    print("Ответ от Avito API:", response.status_code, response.text)

    # Пробуем вернуть токен
    return response.json()["access_token"]
