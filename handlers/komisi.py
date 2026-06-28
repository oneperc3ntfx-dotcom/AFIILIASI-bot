from telegram import Update
from telegram.ext import ContextTypes
from appscript import get_komisi

async def komisi_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    data = get_komisi(user_id)

    if not data.get("success"):
        await update.message.reply_text(data.get("message"))
        return

    msg = f"""
💰 INFO KOMISI

Wallet: {data['wallet']}
Komisi: ${data['komisi']}

Bank: {data['bank'] or '-'}
Nama: {data['namaRekening'] or '-'}
Rekening: {data['rekening'] or '-'}

Status Rekening:
{'✅ Lengkap' if data['bankComplete'] else '❌ Belum Lengkap'}
"""

    await update.message.reply_text(msg)
