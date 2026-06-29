from telegram import ReplyKeyboardMarkup


def main_menu():

    keyboard = [

        ["💰 Komisi", "🏦 Withdraw"],

        ["📞 Support", "ℹ️ Bantuan"]

    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        one_time_keyboard=False,
        selective=False
    )
