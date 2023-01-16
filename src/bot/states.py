from telegram.ext import ConversationHandler


"""Константы ConversationHandler"""
(
    SELECTING_ACTION,
    CHATS,
    REQUEST,
    ADD_VOLUNTEER,
    TELL_ABOUT_FUND,
    DONATION,
    EVENTS,
    QUESTION,
    ABOUT,
) = map(chr, range(9))

(
    VOLUNTEER,
    ADDING_VOLUNTEER,
    ADDING_NAME,
    ADDING_BIRTHDAY,
    ADDING_CITY,
    ADDING_PHONE,
    ADDING_EMAIL,
    ADDING_MESSAGE,
    SHOWING_VOLUNTEER,
    EDIT_VOLUNTEER,
    VOLUNTEER_FEATURE,
    TYPING_VOLUNTEER,
    SEND_VOLUNTEER,
    VOLUNTEER_SENT,
    SENT,
) = map(chr, range(10, 25))

(STOPPING,) = map(chr, range(30, 31))

(
    WEBSITE,
    VK,
    INSTAGRAM,
    FACEBOOK,
    TG_CHANNEL,
    TG_BOT,
) = map(chr, range(50, 56))

(
    START_OVER,
    CURRENT_FEATURE,
    LEVEL,
    FEATURES,
    NAME,
    BIRTHDAY,
    CITY,
    PHONE,
    EMAIL,
    MESSAGE,
) = map(chr, range(100, 110))

END = ConversationHandler.END
