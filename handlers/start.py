import re

from telegram import Update
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
    CommandHandler,
    MessageHandler,
    filters,
)

from states import WALLET, GMAIL
from keyboards.menu import main_menu
from appscript import register


# =========================
# START
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data.clear()

    await update.message.reply_text(
        "👋 Selamat Datang.\n\n"
        "Silakan masukkan ID Wallet Anda."
    )

    return WALLET


# =========================
# INPUT WALLET
# =========================
async def wallet(update: Update, context: ContextTypes.DEFAULT_TYPE):

    wallet = update.message.text.strip().upper()

    if len(wallet) < 3:
        await update.message.reply_text(
            "❌ ID Wallet tidak valid.\n\nSilakan masukkan kembali."
        )
        return WALLET

    context.user_data["wallet"] = wallet

    await update.message.reply_text(
        "📧 Sekarang masukkan Gmail yang terdaftar pada broker."
    )

    return GMAIL


# =========================
# INPUT GMAIL
# =========================
async def gmail(update: Update, context: ContextTypes.DEFAULT_TYPE):

    gmail = update.message.text.strip().lower()

    if not re.match(r"^[^@]+@[^@]+\.[^@]+$", gmail):

        await update.message.reply_text(
            "❌ Format Gmail tidak valid.\n\nSilakan masukkan kembali."
        )

        return GMAIL

    wallet = context.user_data["wallet"]
    telegram = str(update.effective_user.id)

    try:

        result = register(
            wallet,
            gmail,
            telegram
        )

    except Exception:

        await update.message.reply_text(
            "❌ Server sedang bermasalah.\nSilakan coba beberapa saat lagi."
        )

        return ConversationHandler.END

    if result.get("success"):

        await update.message.reply_text(
            f"""✅ Registrasi berhasil

👛 Wallet :
{wallet}

Selamat datang di sistem Affiliate.
""",
            reply_markup=main_menu()
        )

    else:

        await update.message.reply_text(
            result.get("message", "Terjadi kesalahan.")
        )

    return ConversationHandler.END


# =========================
# CANCEL
# =========================
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data.clear()

    await update.message.reply_text(
        "❌ Registrasi dibatalkan."
    )

    return ConversationHandler.END


register_handler = ConversationHandler(

    entry_points=[
        CommandHandler("start", start)
    ],

    states={

        WALLET: [

            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                wallet
            )

        ],

        GMAIL: [

            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                gmail
            )

        ]

    },

    fallbacks=[
        CommandHandler("cancel", cancel)
    ],

    allow_reentry=True

)
