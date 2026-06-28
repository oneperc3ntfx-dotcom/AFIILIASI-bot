from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
)

from config import BOT_TOKEN
from handlers.start import start
from handlers.komisi import komisi
from handlers.withdraw import withdraw


def main():

    app = Application.builder().token(BOT_TOKEN).build()

    # Command
    app.add_handler(CommandHandler("start", start))

    # Button
    app.add_handler(MessageHandler(filters.Regex("^💰 Cek Komisi$"), komisi))
    app.add_handler(MessageHandler(filters.Regex("^🏦 Withdraw$"), withdraw))

    print("Bot Running...")

    app.run_polling()


if __name__ == "__main__":
    main()
