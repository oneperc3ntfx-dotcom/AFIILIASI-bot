import requests

from config import APPSCRIPT_URL

TIMEOUT = 20


# ==========================================
# REQUEST
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

        # Apps Script menggunakan camelCase
        "namaRekening": nama_rekening,

        "rekening": rekening

    })


# ==========================================
# APPROVE
# ==========================================

def approve_withdraw(wd_id):

    return _request({

        "action": "approveWithdraw",

        "wdId": wd_id

    })


# ==========================================
# REJECT
# ==========================================

def reject_withdraw(wd_id):

    return _request({

        "action": "rejectWithdraw",

        "wdId": wd_id

    })
