import logging

from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    MessageHandler,
    filters,
)

from config import BOT_TOKEN

from handlers.start import register_handler
from handlers.withdraw import withdraw_handler
from handlers.komisi import komisi_cmd
from handlers.admin import admin_callback

from keyboards.menu import main_menu


# ==========================================
# LOGGING
# ==========================================

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

logger = logging.getLogger(__name__)


# ==========================================
# MENU SUPPORT
# ==========================================

async def support(update, context):

    await update.message.reply_text(
        """
📞 CUSTOMER SUPPORT

Jika mengalami kendala mengenai:

• Registrasi
• Komisi
• Withdraw
• Akun Affiliate

Silakan hubungi Admin.

👉 https://t.me/USERNAME_ADMIN
"""
    )


# ==========================================
# MENU BANTUAN
# ==========================================

async def bantuan(update, context):

    await update.message.reply_text(
        """
ℹ️ PANDUAN

1️⃣ Ketik /start untuk registrasi.

2️⃣ Setelah berhasil registrasi,
gunakan menu:

💰 Komisi
untuk melihat saldo komisi.

🏦 Withdraw
untuk melakukan withdraw.

3️⃣ Withdraw akan diproses Admin.

4️⃣ Setelah disetujui atau ditolak,
Anda akan menerima notifikasi otomatis.
"""
    )


# ==========================================
# ERROR HANDLER
# ==========================================

async def error_handler(update, context):

    logger.error("Exception", exc_info=context.error)

    if update and update.effective_message:

        await update.effective_message.reply_text(
            "❌ Terjadi kesalahan pada server.\nSilakan coba kembali."
        )


# ==========================================
# MAIN
# ==========================================

def main():

    app = Application.builder().token(BOT_TOKEN).build()

    # Conversation
    app.add_handler(register_handler)
    app.add_handler(withdraw_handler)

    # Menu
    app.add_handler(

        MessageHandler(
            filters.Regex("^💰 Komisi$"),
            komisi_cmd
        )

    )

    app.add_handler(

        MessageHandler(
            filters.Regex("^📞 Support$"),
            support
        )

    )

    app.add_handler(

        MessageHandler(
            filters.Regex("^ℹ️ Bantuan$"),
            bantuan
        )

    )

    # Admin Button
    app.add_handler(

        CallbackQueryHandler(
            admin_callback,
            pattern="^wd_(done|reject):"
        )

    )

    # Error
    app.add_error_handler(error_handler)

    logger.info("Bot Running...")

    app.run_polling(
        drop_pending_updates=True
    )


if __name__ == "__main__":
    main()
