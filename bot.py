import logging
from telegram.ext import Application, CommandHandler

from config import BOT_TOKEN

from handlers.start import start_cmd
from handlers.komisi import komisi_cmd
from handlers.withdraw import withdraw_start, withdraw_handler


# =========================
# LOGGING (WAJIB untuk debug Railway)
# =========================
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

logger = logging.getLogger(__name__)


# =========================
# MAIN APP
# =========================
app = Application.builder().token(BOT_TOKEN).build()


# =========================
# COMMAND HANDLERS
# =========================
app.add_handler(CommandHandler("start", start_cmd))
app.add_handler(CommandHandler("komisi", komisi_cmd))
app.add_handler(CommandHandler("withdraw", withdraw_start))


# =========================
# CONVERSATION HANDLER (withdraw flow)
# =========================
app.add_handler(withdraw_handler)


# =========================
# START BOT
# =========================
if __name__ == "__main__":
    print("🤖 BOT RUNNING...")
    app.run_polling()
