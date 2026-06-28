from telegram import Update
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from services.appscript import get_profile, withdraw
from states import BANK, REKENING, NOMINAL

# ==========================
# Tombol Withdraw
# ==========================

async def withdraw_start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    telegram = str(update.effective_user.id)

    profile = get_profile(telegram)

    if not profile["success"]:
        await update.message.reply_text(profile["message"])
        return ConversationHandler.END

    context.user_data["profile"] = profile

    # Bank belum ada
    if profile["bank"] == "" or profile["rekening"] == "":

        await update.message.reply_text(
            "Masukkan Nama Bank."
        )

        return BANK

    await update.message.reply_text(
        "Masukkan nominal Withdraw (USD)."
    )

    return NOMINAL


# ==========================
# Input Bank
# ==========================

async def bank(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["bank"] = update.message.text.strip()

    await update.message.reply_text(
        "Masukkan Nomor Rekening."
    )

    return REKENING


# ==========================
# Input Rekening
# ==========================

async def rekening(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["rekening"] = update.message.text.strip()

    await update.message.reply_text(
        "Masukkan Nominal Withdraw."
    )

    return NOMINAL


# ==========================
# Input Nominal
# ==========================

async def nominal(update: Update, context: ContextTypes.DEFAULT_TYPE):

    telegram = str(update.effective_user.id)

    profile = context.user_data["profile"]

    bank = profile["bank"]
    rekening = profile["rekening"]

    if bank == "":
        bank = context.user_data["bank"]

    if rekening == "":
        rekening = context.user_data["rekening"]

    nominal = update.message.text.strip()

    result = withdraw(
        telegram,
        nominal,
        bank,
        rekening
    )

    if result["success"]:

        text = (
            "✅ Withdraw Berhasil\n\n"
            f"Nominal : ${result['nominal']}\n"
            f"Sisa Komisi : ${result['sisaKomisi']}\n"
            f"Status : {result['status']}"
        )

        await update.message.reply_text(text)

    else:

        await update.message.reply_text(result["message"])

    return ConversationHandler.END


# ==========================
# Handler
# ==========================

withdraw_handler = ConversationHandler(

    entry_points=[

        MessageHandler(
            filters.Regex("^🏦 Withdraw$"),
            withdraw_start
        )

    ],

    states={

        BANK: [

            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                bank
            )

        ],

        REKENING: [

            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                rekening
            )

        ],

        NOMINAL: [

            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                nominal
            )

        ]

    },

    fallbacks=[]

)
