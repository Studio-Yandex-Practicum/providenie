from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
)

from bot import states
from bot.conversations import menu


tell_about_fund_conv = ConversationHandler(
    name="tell_about_fund_conv",
    allow_reentry=True,
    entry_points=[
        CallbackQueryHandler(
            menu.tell_friends_about_fund,
            pattern="^" + str(states.TELL_ABOUT_FUND) + "$",
        )
    ],
    states={
        states.SOCIAL_LINKS: [
            CallbackQueryHandler(
                menu.social_link,
                pattern=(
                    "^"
                    + "$|^".join(
                        [
                            states.WEBSITE,
                            states.VK,
                            states.INSTAGRAM,
                            states.FACEBOOK,
                            states.TG_CHANNEL,
                            states.TG_BOT,
                        ]
                    )
                    + "$"
                ),
            )
        ]
    },
    fallbacks=[
        CallbackQueryHandler(
            menu.end_second_level, pattern="^" + str(states.END) + "$"
        ),
        CommandHandler("stop", menu.stop),
    ],
)
