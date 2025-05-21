import requests
import time
import os
from auth import get_avito_token

TOGETHER_API_KEY = os.getenv("dac2b7680df5189a3b719391c7fdf26463aa4db874a51a5ea7d3a27395112a84")
CLIENT_ID = os.getenv("dV-ZACda-zl__NNkQmpo")
CLIENT_SECRET = os.getenv("NXZ3jj-CQyEZFjkBmJpQiR7RPQ4QU8fMh7AA4pR-")
AVITO_USER_ID = "2f4d44af0946d32df3f9fe920ba92f81"  # можно указать ID продавца

def generate_ai_response(prompt):
    url = "https://api.together.xyz/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "mistralai/Mistral-7B-Instruct-v0.1",
        "messages": [
            {"role": "system", "content": "Ты — помощник продавца на Авито."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 200
    }
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()['choices'][0]['message']['content']

def get_chats(token):
    url = f"https://api.avito.ru/messenger/v2/accounts/{AVITO_USER_ID}/chats"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json().get("chats", [])

def get_messages(token, chat_id):
    url = f"https://api.avito.ru/messenger/v3/accounts/{AVITO_USER_ID}/chats/{chat_id}/messages?limit=5"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def send_message(token, chat_id, text):
    url = f"https://api.avito.ru/messenger/v1/accounts/{AVITO_USER_ID}/chats/{chat_id}/messages"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "type": "text",
        "message": {
            "text": text
        }
    }
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()

def main():
    token = get_avito_token(CLIENT_ID, CLIENT_SECRET)
    processed_ids = set()

    print("Бот запущен. Ожидание новых сообщений...")

    while True:
        try:
            chats = get_chats(token)
            for chat in chats:
                chat_id = chat["id"]
                messages = get_messages(token, chat_id)
                for message in messages:
                    if message["direction"] == "in" and message["id"] not in processed_ids:
                        text = message["content"].get("text")
                        if text:
                            print(f"Новое сообщение: {text}")
                            reply = generate_ai_response(text)
                            print(f"Ответ: {reply}")
                            send_message(token, chat_id, reply)
                            processed_ids.add(message["id"])
            time.sleep(5)
        except Exception as e:
            print(f"Ошибка: {e}")
            time.sleep(10)

if __name__ == "__main__":
    main()