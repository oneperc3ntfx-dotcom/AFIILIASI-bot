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

# IMPORT APPSCRIPT (PASTIKAN INI ADA DI ROOT PROJECT)
from appscript import register


# =========================
# STEP 1: START COMMAND
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "👋 Selamat Datang.\n\nMasukkan ID Wallet Anda."
    )

    return WALLET


# =========================
# STEP 2: INPUT WALLET
# =========================
async def wallet(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["wallet"] = update.message.text.strip()

    await update.message.reply_text(
        "Sekarang masukkan Gmail yang terdaftar pada broker."
    )

    return GMAIL


# =========================
# STEP 3: INPUT GMAIL + REGISTER
# =========================
async def gmail(update: Update, context: ContextTypes.DEFAULT_TYPE):

    wallet = context.user_data.get("wallet")
    gmail = update.message.text.strip()
    telegram = str(update.effective_user.id)

    # CALL APPSCRIPT REGISTER
    result = register(wallet, gmail, telegram)

    if result.get("success"):

        await update.message.reply_text(
            "✅ Registrasi berhasil.",
            reply_markup=main_menu()
        )

        return ConversationHandler.END

    await update.message.reply_text(
        result.get("message", "Terjadi kesalahan.")
    )

    return ConversationHandler.END


# =========================
# CANCEL COMMAND
# =========================
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text("❌ Registrasi dibatalkan.")

    return ConversationHandler.END


# =========================
# CONVERSATION HANDLER
# =========================
register_handler = ConversationHandler(

    entry_points=[
        CommandHandler("start", start)
    ],

    states={
        WALLET: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, wallet)
        ],

        GMAIL: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, gmail)
        ]
    },

    fallbacks=[
        CommandHandler("cancel", cancel)
    ]
)
