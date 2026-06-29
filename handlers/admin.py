from telegram import Update
from telegram.ext import ContextTypes

from appscript import approve_withdraw, reject_withdraw


async def admin_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    try:

        action, wd_id, telegram = query.data.split(":")

    except ValueError:

        await query.edit_message_text(
            "❌ Data callback tidak valid."
        )

        return

    # ==========================================
    # APPROVE
    # ==========================================

    if action == "wd_done":

        result = approve_withdraw(wd_id)

        if result.get("success"):

            # Edit pesan di grup admin
            await query.edit_message_text(
                f"""✅ WITHDRAW APPROVED

🆔 WD ID
{wd_id}

Status : Done"""
            )

            # Kirim ke user
            try:

                await context.bot.send_message(

                    chat_id=int(telegram),

                    text=f"""✅ Withdraw Berhasil Diproses

🆔 WD ID
{wd_id}

Status
Done

Dana Anda sedang diproses ke rekening yang terdaftar.

Terima kasih telah menggunakan layanan kami."""

                )

            except Exception as e:

                print(e)

        else:

            await query.edit_message_text(
                f"""❌ Gagal Approve

{result.get("message")}"""
            )

        return

    # ==========================================
    # REJECT
    # ==========================================

    if action == "wd_reject":

        result = reject_withdraw(wd_id)

        if result.get("success"):

            # Edit pesan di grup admin
            await query.edit_message_text(
                f"""❌ WITHDRAW REJECTED

🆔 WD ID
{wd_id}

Status : Rejected"""
            )

            # Kirim ke user
            try:

                await context.bot.send_message(

                    chat_id=int(telegram),

                    text=f"""❌ Withdraw Ditolak

🆔 WD ID
{wd_id}

Status
Rejected

💰 Saldo komisi Anda telah dikembalikan.

Silakan hubungi Admin:

👉 @ONEPercentsFX"""

                )

            except Exception as e:

                print(e)

        else:

            await query.edit_message_text(
                f"""❌ Gagal Reject

{result.get("message")}"""
            )

        return
