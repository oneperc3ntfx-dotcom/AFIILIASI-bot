from telegram import ReplyKeyboardMarkup
from config import ADMIN_IDS


def main_menu(user_id=None):

    keyboard = [

        ["💰 Komisi", "🏦 Withdraw"],

        ["📞 Support", "ℹ️ Bantuan"]

    ]

    if user_id in ADMIN_IDS:
        keyboard.append(["🛠 Admin Panel"])

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        one_time_keyboard=False
    )
