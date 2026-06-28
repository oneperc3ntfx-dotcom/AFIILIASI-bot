from telegram import Update
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from services.appscript import get_komisi, withdraw
from states import BANK, REKENING, NOMINAL


async def withdraw_start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    telegram = str(update.effective_user.id)

    result = get_komisi(telegram)

    if not result["success"]:
        await update.message.reply_text(result["message"])
        return ConversationHandler.END

    context.user_data["wallet"] = result["wallet"]
    context.user_data["bank"] = result["bank"]
    context.user_data["rekening"] = result["rekening"]

    if result["bank"] == "" or result["rekening"] == "":

        await update.message.reply_text(
            "Silahkan masukkan Nama Bank."
        )

        return BANK

    await update.message.reply_text(
        "Masukkan nominal Withdraw (USD)."
    )

    return NOMINAL


async def bank(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["bank"] = update.message.text.strip()

    await update.message.reply_text(
        "Masukkan Nomor Rekening."
    )

    return REKENING


async def rekening(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["rekening"] = update.message.text.strip()

    await update.message.reply_text(
        "Masukkan nominal Withdraw."
    )

    return NOMINAL


async def nominal(update: Update, context: ContextTypes.DEFAULT_TYPE):

    telegram = str(update.effective_user.id)

    nominal = update.message.text.strip()

    bank = context.user_data["bank"]
    rekening = context.user_data["rekening"]

    result = withdraw(
        telegram,
        nominal,
        bank,
        rekening
    )

    if result["success"]:

        text = f"""
✅ Withdraw Berhasil

💵 Nominal : ${result['nominal']}

💰 Sisa Komisi : ${result['sisaKomisi']}

🏦 Bank : {result['bank']}

📋 Status : {result['status']}
"""

        await update.message.reply_text(text)

    else:

        await update.message.reply_text(result["message"])

    return ConversationHandler.END


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
