from telegram import Update
from telegram.ext import ContextTypes

from services.appscript import get_komisi


async def komisi_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):

    telegram = str(update.effective_user.id)

    try:
        data = get_komisi(telegram)

    except Exception:
        await update.message.reply_text(
            "❌ Tidak dapat terhubung ke server.\nSilakan coba beberapa saat lagi."
        )
        return

    if not data.get("success", False):
        await update.message.reply_text(
            data.get("message", "Terjadi kesalahan.")
        )
        return

    wallet = data.get("wallet", "-")
    komisi = float(data.get("komisi", 0))
    bank = data.get("bank") or "-"
    nama = data.get("namaRekening") or "-"
    rekening = data.get("rekening") or "-"

    bank_complete = data.get("bankComplete")

    if bank_complete is None:
        bank_complete = (
            bank != "-" and
            nama != "-" and
            rekening != "-"
        )

    text = (
        "💰 <b>INFO KOMISI</b>\n\n"
        f"👛 <b>Wallet</b>\n{wallet}\n\n"
        f"💵 <b>Komisi</b>\n${komisi:,.2f}\n\n"
        f"🏦 <b>Bank</b>\n{bank}\n\n"
        f"👤 <b>Nama Rekening</b>\n{nama}\n\n"
        f"💳 <b>No. Rekening</b>\n{rekening}\n\n"
        f"📋 <b>Status Rekening</b>\n"
        f"{'✅ Lengkap' if bank_complete else '❌ Belum Lengkap'}"
    )

    await update.message.reply_text(
        text,
        parse_mode="HTML"
    )
