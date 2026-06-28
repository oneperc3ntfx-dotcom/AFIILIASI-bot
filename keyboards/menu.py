from telegram import ReplyKeyboardMarkup


def main_menu():
    keyboard = [
        ["💰 Cek Komisi"],
        ["🏦 Withdraw"]
    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        one_time_keyboard=False
    )
