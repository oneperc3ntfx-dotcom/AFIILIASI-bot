from telegram import Update
from telegram.ext import ContextTypes

from services.appscript import approve_withdraw, reject_withdraw


async def admin_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    data = query.data

    try:
        action, wd_id = data.split(":")
    except ValueError:
        await query.edit_message_text("❌ Data callback tidak valid.")
        return

    if action == "wd_done":

        result = approve_withdraw(wd_id)

        if result.get("success"):

            text = f"""✅ WITHDRAW APPROVED

🆔 WD ID : {wd_id}

Status : Done
"""

        else:

            text = f"""❌ Gagal approve

{result.get("message")}
"""

        await query.edit_message_text(text)

        return

    if action == "wd_reject":

        result = reject_withdraw(wd_id)

        if result.get("success"):

            text = f"""❌ WITHDRAW REJECTED

🆔 WD ID : {wd_id}

Saldo member telah dikembalikan.
"""

        else:

            text = f"""❌ Gagal reject

{result.get("message")}
"""

        await query.edit_message_text(text)
