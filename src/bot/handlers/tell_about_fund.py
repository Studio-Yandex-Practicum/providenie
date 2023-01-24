from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
)

from bot import keys, states
from bot.conversations import menu


tell_about_fund_conv = ConversationHandler(
    name="tell_about_fund_conv",
    allow_reentry=True,
    entry_points=[
        CallbackQueryHandler(
            menu.tell_friends_about_fund,
            pattern="^" + keys.TELL_ABOUT_FUND + "$",
        )
    ],
    states={
        states.SOCIAL_LINKS: [
            CallbackQueryHandler(menu.social_link, pattern=r"^TELL_ABOUT_\S*$")
        ]
    },
    fallbacks=[
        CallbackQueryHandler(
            menu.end_second_level, pattern="^" + str(keys.END) + "$"
        ),
        CommandHandler("stop", menu.stop),
    ],
)
