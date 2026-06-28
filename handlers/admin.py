from telegram import Update
from telegram.ext import ContextTypes

# contoh sederhana (pakai command dulu)
# nanti bisa kita upgrade jadi button inline

async def approve(update: Update, context: ContextTypes.DEFAULT_TYPE):

    wd_id = context.args[0]

    await update.message.reply_text(f"✅ WD {wd_id} sudah DIAPPROVE")


async def reject(update: Update, context: ContextTypes.DEFAULT_TYPE):

    wd_id = context.args[0]

    await update.message.reply_text(f"❌ WD {wd_id} DITOLAK + refund diproses")
