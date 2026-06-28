from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
)

from config import BOT_TOKEN
from handlers.start import register_handler
from handlers.komisi import komisi
from handlers.withdraw import withdraw_handler


def main():

    app = Application.builder().token(BOT_TOKEN).build()

    # Command
    app.add_handler(register_handler)

    # Button
    app.add_handler(MessageHandler(filters.Regex("^💰 Cek Komisi$"), komisi))
    app.add_handler(withdraw_handler)

    print("Bot Running...")

    app.run_polling()


if __name__ == "__main__":
    main()
