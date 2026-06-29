from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def withdraw_admin_keyboard(
    wd_id,
    telegram
):
    keyboard = [
        [
            InlineKeyboardButton(
                "✅ Done",
                callback_data=f"wd_done:{wd_id}"
            ),
            InlineKeyboardButton(
                "❌ Reject",
                callback_data=f"wd_reject:{wd_id}"
            )
        ]
    ]

    return InlineKeyboardMarkup(keyboard)
