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

    # 🔍 Показываем реальный ответ от Avito
    print("Ответ от Avito API:", response.status_code)
    print("Тело ответа:", response.text)

    if response.status_code != 200 or "access_token" not in response.json():
        raise Exception("Не удалось получить access_token")

    return response.json()["access_token"]
