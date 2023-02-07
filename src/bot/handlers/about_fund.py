from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
)

from bot import keys, states
from bot.conversations import about_fund, menu


about_fund_conv = ConversationHandler(
    name="about_fund_conv",
    allow_reentry=True,
    entry_points=[
        CallbackQueryHandler(
            about_fund.select_about_found,
            pattern="^" + keys.ABOUT_FUND + "$",
        ),
        CallbackQueryHandler(
            about_fund.select_success_found,
            pattern="^" + keys.ABOUT_SUCCESS + "$",
        ),
    ],
    states={
        states.ABOUT_INFO: [
            CallbackQueryHandler(menu.about, pattern=r"^ABOUT_\S*$")
        ]
    },
    fallbacks=[
        CallbackQueryHandler(
            menu.end_second_level, pattern="^" + str(keys.END) + "$"
        ),
        CommandHandler("stop", menu.stop),
    ],
)
