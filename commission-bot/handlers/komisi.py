from telegram import Update
from telegram.ext import ContextTypes

from services.appscript import get_komisi


async def komisi(update: Update, context: ContextTypes.DEFAULT_TYPE):

    telegram = str(update.effective_user.id)

    result = get_komisi(telegram)

    if not result["success"]:
        await update.message.reply_text(result["message"])
        return

    text = (
        "💰 <b>Informasi Komisi</b>\n\n"
        f"🆔 ID Wallet : <code>{result['wallet']}</code>\n"
        f"💵 Komisi : <b>${result['komisi']}</b>"
    )

    await update.message.reply_text(
        text,
        parse_mode="HTML"
    )
