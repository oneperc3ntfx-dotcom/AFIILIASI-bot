from telegram import Update
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from config import ADMIN_GROUP_ID
from keyboards.admin import withdraw_admin_keyboard
from services.appscript import get_komisi, withdraw
from states import BANK, REKENING, NOMINAL


# ==========================
# START WITHDRAW
# ==========================

async def withdraw_start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    telegram = str(update.effective_user.id)

    try:
        result = get_komisi(telegram)

    except Exception:
        await update.message.reply_text(
            "❌ Server sedang bermasalah.\nSilakan coba beberapa saat lagi."
        )
        return ConversationHandler.END

    if not result.get("success"):

        await update.message.reply_text(
            result.get("message")
        )

        return ConversationHandler.END

    context.user_data["wallet"] = result.get("wallet")
    context.user_data["bank"] = result.get("bank") or ""
    context.user_data["rekening"] = result.get("rekening") or ""

    if (
        context.user_data["bank"] == ""
        or
        context.user_data["rekening"] == ""
    ):

        await update.message.reply_text(
            "🏦 Data rekening belum tersedia.\n\nMasukkan Nama Bank."
        )

        return BANK

    await update.message.reply_text(
        f"""💰 Komisi Anda : ${float(result.get("komisi",0)):,.2f}

Masukkan nominal Withdraw (USD)."""
    )

    return NOMINAL


# ==========================
# INPUT BANK
# ==========================

async def bank(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["bank"] = update.message.text.strip()

    await update.message.reply_text(
        "Masukkan Nomor Rekening."
    )

    return REKENING


# ==========================
# INPUT REKENING
# ==========================

async def rekening(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["rekening"] = update.message.text.strip()

    await update.message.reply_text(
        "Masukkan Nominal Withdraw."
    )

    return NOMINAL


# ==========================
# INPUT NOMINAL
# ==========================

async def nominal(update: Update, context: ContextTypes.DEFAULT_TYPE):

    telegram = str(update.effective_user.id)

    text = update.message.text.strip()

    try:
        nominal = float(text)

    except ValueError:

        await update.message.reply_text(
            "❌ Nominal harus berupa angka."
        )

        return NOMINAL

    if nominal <= 0:

        await update.message.reply_text(
            "❌ Nominal tidak valid."
        )

        return NOMINAL

    bank = context.user_data["bank"]
    rekening = context.user_data["rekening"]

    try:

        result = withdraw(
            telegram=telegram,
            nominal=nominal,
            bank=bank,
            rekening=rekening
        )

    except Exception:

        await update.message.reply_text(
            "❌ Server sedang bermasalah."
        )

        return ConversationHandler.END

    if not result.get("success"):

        await update.message.reply_text(
            result.get("message")
        )

        return ConversationHandler.END

    # ==========================
    # USER MESSAGE
    # ==========================

    await update.message.reply_text(
        f"""
✅ Withdraw Berhasil

🆔 WD ID :
{result['wdId']}

💵 Nominal :
${float(result['nominal']):,.2f}

💰 Sisa Komisi :
${float(result['sisaKomisi']):,.2f}

🏦 Bank :
{result['bank']}

📋 Status :
{result['status']}
"""
    )

    # ==========================
    # ADMIN GROUP
    # ==========================

    admin_text = f"""
📥 REQUEST WITHDRAW

🆔 WD ID :
{result['wdId']}

👛 Wallet :
{result['wallet']}

👤 Telegram :
{telegram}

💵 Nominal :
${float(result['nominal']):,.2f}

🏦 Bank :
{result['bank']}

💳 Rekening :
{result['rekening']}

📋 Status :
{result['status']}
"""

    await context.bot.send_message(

        chat_id=ADMIN_GROUP_ID,

        text=admin_text,

        reply_markup=withdraw_admin_keyboard(
            result["wdId"]
        )

    )

    return ConversationHandler.END


# ==========================
# HANDLER
# ==========================

withdraw_handler = ConversationHandler(

    entry_points=[

        MessageHandler(
            filters.Regex("^🏦 Withdraw$"),
            withdraw_start
        )

    ],

    states={

        BANK:[

            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                bank
            )

        ],

        REKENING:[

            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                rekening
            )

        ],

        NOMINAL:[

            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                nominal
            )

        ]

    },

    fallbacks=[],

    allow_reentry=True

)
