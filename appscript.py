import requests
from config import APPSCRIPT_URL


# =========================
# REGISTER MEMBER (FIX BARU)
# =========================
def register(wallet, gmail, telegram):

    r = requests.get(APPSCRIPT_URL, params={
        "action": "register",
        "wallet": wallet,
        "gmail": gmail,
        "telegram": telegram
    })

    return r.json()


# =========================
# CEK KOMISI
# =========================
def get_komisi(telegram_id):

    r = requests.get(APPSCRIPT_URL, params={
        "action": "komisi",
        "telegram": telegram_id
    })

    return r.json()


# =========================
# WITHDRAW
# =========================
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
