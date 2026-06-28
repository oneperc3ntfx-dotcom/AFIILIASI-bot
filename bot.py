from telegram.ext import Application
from config import BOT_TOKEN

from handlers.komisi import komisi_cmd
from handlers.withdraw import withdraw_handler

app = Application.builder().token(BOT_TOKEN).build()

# command
app.add_handler(komisi_cmd)

# withdraw flow
app.add_handler(withdraw_handler)

print("Bot running...")
app.run_polling()
