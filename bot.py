import logging
from telegram.ext import (
    Application,
    CommandHandler,
)

from config import BOT_TOKEN

from handlers.start import register_handler
from handlers.komisi import komisi_cmd
from handlers.withdraw import withdraw_start, withdraw_handler


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

app = Application.builder().token(BOT_TOKEN).build()

# REGISTER FLOW (/start)
app.add_handler(register_handler)

# COMMANDS
app.add_handler(CommandHandler("komisi", komisi_cmd))
app.add_handler(CommandHandler("withdraw", withdraw_start))

# WITHDRAW FLOW
app.add_handler(withdraw_handler)

print("🤖 BOT RUNNING...")
app.run_polling()
