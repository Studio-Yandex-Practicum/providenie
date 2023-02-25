from bot.constants import key
from bot.constants.info import option
from bot.conversations.models import (AskQuestionForm, ChatForm, FundForm,
                                      VolunteerForm)


ALL_MENU = {
    f"{key.MENU}_CHAT": {
        key.BUTTON_TEXT: "Хочу попасть в родительский чат",
        key.DESCRIPTION: "Выберите чат для вступления:",
        key.MODEL: ChatForm,
        key.FIELDS: list(ChatForm.__fields__),
        key.OPTIONS: option.CHAT,
    },
    f"{key.MENU}_FOND": {
        key.BUTTON_TEXT: "Заявка в фонд",
        key.DESCRIPTION: "Выберите программу фонда или вернитесь обратно в главное меню:",
        key.MODEL: FundForm,
        key.FIELDS: list(FundForm.__fields__),
        key.OPTIONS: option.FUND,
    },
    f"{key.MENU}_VOLONTEER": {
        key.BUTTON_TEXT: "Хочу стать волонтёром",
        key.DESCRIPTION: "Далее необходимо предоставить информацию для куратора",
        key.MODEL: VolunteerForm,
        key.FIELDS: list(VolunteerForm.__fields__),
    },
    f"{key.MENU}_ASK_QUESTION": {
        key.BUTTON_TEXT: "Задать вопрос",
        key.DESCRIPTION: "Далее необходимо заполнить поля для вопроса",
        key.MODEL: AskQuestionForm,
        key.FIELDS: list(AskQuestionForm.__fields__),
    },
    f"{key.MENU}_SHARE": {
        key.BUTTON_TEXT: "Поделится",
        key.DESCRIPTION: "БЛА БЛА",
        key.OPTIONS: option.SHARE,
    },
    f"{key.MENU}_DONATION": {
        key.BUTTON_TEXT: "Отчеты и пожертвования",
        key.DESCRIPTION: "БЛА БЛА БЛА",
        key.OPTIONS: option.DONATION,
    },
    f"{key.MENU}_ABOUT": {
        key.BUTTON_TEXT: "О Фонде",
        key.DESCRIPTION: "БЛА БЛА",
        key.OPTIONS: option.ABOUT,
    },
}
