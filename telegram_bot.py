import requests
from config import BOT_TOKEN, ADMIN_ID


def send_code(code):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    requests.post(
        url,
        data={
            "chat_id": ADMIN_ID,
            "text": f"🔐 Tasdiqlash kodi: {code}"
        }
    )