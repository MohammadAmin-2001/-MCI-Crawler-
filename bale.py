import os
import requests


BALE_BOT_TOKEN = os.getenv("BALE_BOT_TOKEN")
BASE_URL = f"https://tapi.bale.ai/bot{BALE_BOT_TOKEN}"

def send_bale_message(message: str,chat_id:int):
    url = f"{BASE_URL}/sendMessage"

    payload = {
        "chat_id": chat_id,
        "text": message,
    }

    response = requests.post(
        url,
        json=payload,
        timeout=10,
    )

    response.raise_for_status()

    data = response.json()

    if not data.get("ok"):
        raise RuntimeError(data)

    return data

def get_ids():
    response = requests.get(
    f"{BASE_URL}/getUpdates",
    timeout=10
)

    data = response.json()

    chat_ids = set()

    for update in data.get("result", []):
        message = update.get("message")

        if message:
            chat = message.get("chat", {})
            chat_id = chat.get("id")

            if chat_id is not None:
                chat_ids.add(chat_id)

    return chat_ids

