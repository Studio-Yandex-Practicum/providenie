from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
)

from bot import keys, states
from bot.conversations import main_menu


tell_about_fund_conv = ConversationHandler(
    name="tell_about_fund_conv",
    allow_reentry=True,
    entry_points=[
        CallbackQueryHandler(
            main_menu.tell_friends_about_fund,
            pattern="^" + keys.TELL_ABOUT_FUND + "$",
        )
    ],
    states={
        states.SOCIAL_LINKS: [
            CallbackQueryHandler(
                main_menu.social_link, pattern=r"^TELL_ABOUT_\S*$"
            )
        ]
    },
    fallbacks=[
        CallbackQueryHandler(
            main_menu.end_second_level, pattern="^" + str(keys.END) + "$"
        ),
        CommandHandler("stop", main_menu.stop),
    ],
)
