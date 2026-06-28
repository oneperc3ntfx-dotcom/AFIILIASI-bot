import requests
from config import APPSCRIPT_URL

def get_komisi(telegram_id):
    r = requests.get(APPSCRIPT_URL, params={
        "action": "komisi",
        "telegram": telegram_id
    })
    return r.json()


def withdraw(telegram_id, nominal, bank="", namaRekening="", rekening=""):
    r = requests.get(APPSCRIPT_URL, params={
        "action": "withdraw",
        "telegram": telegram_id,
        "nominal": nominal,
        "bank": bank,
        "namaRekening": namaRekening,
        "rekening": rekening
    })
    return r.json()
