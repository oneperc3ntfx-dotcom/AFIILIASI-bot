from telegram import Update
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
    CommandHandler,
    MessageHandler,
    filters,
)

from keyboards.menu import main_menu
from states import WALLET, GMAIL

# ❌ JANGAN IMPORT REGISTER_HANDLER DI SINI

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "👋 Selamat Datang.\n\nMasukkan ID Wallet Anda."
    )

    return WALLET


async def wallet(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["wallet"] = update.message.text.strip()

    await update.message.reply_text(
        "Sekarang masukkan Gmail yang terdaftar pada broker."
    )

    return GMAIL


async def gmail(update: Update, context: ContextTypes.DEFAULT_TYPE):

    wallet = context.user_data["wallet"]
    gmail = update.message.text.strip()
    telegram = str(update.effective_user.id)

    result = register(wallet, gmail, telegram)

    if result["success"]:

        await update.message.reply_text(
            "✅ Registrasi berhasil.",
            reply_markup=main_menu()
        )

        return ConversationHandler.END

    await update.message.reply_text(result["message"])
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text("Registrasi dibatalkan.")
    return ConversationHandler.END


# ✅ REGISTER HANDLER DIBUAT DI DALAM FILE INI (BUKAN IMPORT)
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
