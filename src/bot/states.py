from telegram.ext import ConversationHandler
from .constans.fund_app_constans import GO_MAIN_MENU


"""Константы ConversationHandler"""
(
    SELECTING_ACTION,
    CHATS,
    REQUEST,
    ADD_VOLUNTEER,
    TALK,
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

GO_MAIN_MENU = GO_MAIN_MENU

