import requests
from config import APPS_SCRIPT_URL


def register(wallet, gmail, telegram):
    payload = {
        "action": "register",
        "wallet": wallet,
        "gmail": gmail,
        "telegram": telegram
    }

    r = requests.post(APPS_SCRIPT_URL, data=payload)
    return r.json()


def get_komisi(telegram):
    payload = {
        "action": "komisi",
        "telegram": telegram
    }

    r = requests.post(APPS_SCRIPT_URL, data=payload)
    return r.json()


def withdraw(telegram, nominal, bank="", rekening=""):
    payload = {
        "action": "withdraw",
        "telegram": telegram,
        "nominal": nominal,
        "bank": bank,
        "rekening": rekening
    }

    r = requests.post(APPS_SCRIPT_URL, data=payload)
    return r.json()

def get_profile(telegram):

    payload = {
        "action": "komisi",
        "telegram": telegram
    }

    r = requests.post(APPS_SCRIPT_URL, data=payload)
    return r.json()
