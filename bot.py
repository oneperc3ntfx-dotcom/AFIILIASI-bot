import logging
from telegram.ext import (
    Application,
    CommandHandler,
)

from config import BOT_TOKEN

# handlers
from handlers.start import register_handler
from handlers.komisi import komisi_cmd
from handlers.withdraw import withdraw_start, withdraw_handler


# =========================
# LOGGING (WAJIB DI RAILWAY)
# =========================
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

logger = logging.getLogger(__name__)


# =========================
# INIT APP
# =========================
app = Application.builder().token(BOT_TOKEN).build()


# =========================
# REGISTER HANDLER (START FLOW)
# =========================
app.add_handler(register_handler)


# =========================
# COMMAND HANDLERS
# =========================
app.add_handler(CommandHandler("komisi", komisi_cmd))
app.add_handler(CommandHandler("withdraw", withdraw_start))


# =========================
# WITHDRAW CONVERSATION
# =========================
app.add_handler(withdraw_handler)


# =========================
# RUN BOT
# =========================
if __name__ == "__main__":
    print("🤖 BOT RUNNING...")
    app.run_polling()
