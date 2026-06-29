import requests

from config import APPSCRIPT_URL


TIMEOUT = 20


def _request(payload):

    try:

        response = requests.post(
            APPSCRIPT_URL,
            data=payload,
            timeout=TIMEOUT
        )

        response.raise_for_status()

        return response.json()

    except requests.exceptions.Timeout:

        return {
            "success": False,
            "message": "Server timeout."
        }

    except requests.exceptions.ConnectionError:

        return {
            "success": False,
            "message": "Tidak dapat terhubung ke server."
        }

    except Exception as e:

        return {
            "success": False,
            "message": str(e)
        }


# ============================================
# REGISTER
# ============================================

def register(wallet, gmail, telegram):

    return _request({

        "action": "register",

        "wallet": wallet,

        "gmail": gmail,

        "telegram": telegram

    })


# ============================================
# CEK KOMISI
# ============================================

def get_komisi(telegram):

    return _request({

        "action": "komisi",

        "telegram": telegram

    })


# ============================================
# WITHDRAW
# ============================================

def withdraw(
    telegram,
    nominal,
    bank="",
    namaRekening="",
    rekening=""
):

    return _request({

        "action": "withdraw",

        "telegram": telegram,

        "nominal": nominal,

        "bank": bank,

        "namaRekening": namaRekening,

        "rekening": rekening

    })


# ============================================
# APPROVE WITHDRAW
# ============================================

def approve_withdraw(wd_id):

    return _request({

        "action": "approveWithdraw",

        "wdId": wd_id

    })


# ============================================
# REJECT WITHDRAW
# ============================================

def reject_withdraw(wd_id):

    return _request({

        "action": "rejectWithdraw",

        "wdId": wd_id

    })
