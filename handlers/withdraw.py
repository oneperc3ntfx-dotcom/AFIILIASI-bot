from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler, MessageHandler, filters
from appscript import withdraw

ASK_NOMINAL = 1

async def withdraw_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Masukkan nominal withdraw:")
    return ASK_NOMINAL


async def withdraw_nominal(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id
    nominal = update.message.text

    try:
        nominal = float(nominal)
    except:
        await update.message.reply_text("Nominal tidak valid.")
        return ASK_NOMINAL

    result = withdraw(user_id, nominal)

    # kalau saldo kurang
    if not result.get("success"):

        if result.get("maksimal"):
            await update.message.reply_text(
                f"❌ Saldo tidak cukup\n"
                f"Saldo maksimal: ${result['maksimal']}"
            )
        else:
            await update.message.reply_text(result.get("message"))

        return ConversationHandler.END

    # sukses
    await update.message.reply_text(
        f"""
✅ Withdraw berhasil diajukan

WD ID: {result['wdId']}
Nominal: ${result['nominal']}
Status: Pending

Menunggu approval admin.
"""
    )

    # kirim ke admin group
    from config import ADMIN_GROUP_ID
    from bot import bot

    msg = f"""
🚨 REQUEST WITHDRAW

WD ID: {result['wdId']}
User: {user_id}
Nominal: ${result['nominal']}

Bank: {result['bank']}
Nama: {result['namaRekening']}
Rek: {result['rekening']}
"""

    await bot.send_message(chat_id=ADMIN_GROUP_ID, text=msg)

    return ConversationHandler.END


withdraw_handler = ConversationHandler(
    entry_points=[],
    states={
        ASK_NOMINAL: [MessageHandler(filters.TEXT & ~filters.COMMAND, withdraw_nominal)]
    },
    fallbacks=[]
)
