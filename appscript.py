import requests
from config import APPSCRIPT_URL

TIMEOUT = 20


# ==========================================
# CORE REQUEST
# ==========================================

def _request(payload):
    response = requests.post(
        APPSCRIPT_URL,
        data=payload,
        timeout=TIMEOUT
    )
    response.raise_for_status()
    return response.json()


# ==========================================
# REGISTER
# ==========================================

def register(wallet, gmail, telegram):
    return _request({
        "action": "register",
        "wallet": wallet,
        "gmail": gmail,
        "telegram": telegram
    })


# ==========================================
# KOMISI
# ==========================================

def get_komisi(telegram):
    return _request({
        "action": "komisi",
        "telegram": telegram
    })


# ==========================================
# WITHDRAW
# ==========================================

def withdraw(
    telegram,
    nominal,
    bank="",
    nama_rekening="",
    rekening=""
):
    return _request({
        "action": "withdraw",
        "telegram": telegram,
        "nominal": nominal,
        "bank": bank,
        "namaRekening": nama_rekening,
        "rekening": rekening
    })


# ==========================================
# APPROVE WITHDRAW
# ==========================================

def approve_withdraw(wd_id):
    return _request({
        "action": "approveWithdraw",
        "wdId": wd_id
    })


# ==========================================
# REJECT WITHDRAW
# ==========================================

def reject_withdraw(wd_id):
    return _request({
        "action": "rejectWithdraw",
        "wdId": wd_id
    })


# ==========================================
# GET WITHDRAW BY ID (FIX ERROR KAMU)
# ==========================================

def get_withdraw_by_id(wd_id):
    return _request({
        "action": "getWithdrawById",
        "wdId": wd_id
    })
