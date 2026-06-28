from telegram.ext import Application, CommandHandler

from config import BOT_TOKEN
from handlers.komisi import komisi_cmd

app = Application.builder().token(BOT_TOKEN).build()

# COMMANDS (BENAR)
app.add_handler(CommandHandler("komisi", komisi_cmd))

print("Bot running...")
app.run_polling()
