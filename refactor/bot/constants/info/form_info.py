from bot.constants.info.form_menu import CHAT_MENU, FOND_MENU
from bot.constants import key
from bot.conversations.models import AskQuestionForm, ChatForm, FundForm, VolunteerForm

FORM_INFO = {
    f"{key.FORM}_CHAT": {
        key.BUTTON_TEXT: "Хочу попасть в родительский чат",
        key.DESCRIPTION: "Выберите чат для вступления:",
        key.MODEL: ChatForm,
        key.FIELDS: list(ChatForm.__fields__),
        key.MENU: CHAT_MENU,
    },
    f"{key.FORM}_FOND": {
        key.BUTTON_TEXT: "Заявка в фонд",
        key.DESCRIPTION: "Выберите программу фонда или вернитесь обратно в главное меню:",
        key.MODEL: FundForm,
        key.FIELDS: list(FundForm.__fields__),
        key.MENU: FOND_MENU,
    },
    f"{key.FORM}_VOLONTEER": {
        key.BUTTON_TEXT: "Хочу стать волонтёром",
        key.DESCRIPTION: "Далее необходимо предоставить информацию для куратора",
        key.MODEL: VolunteerForm,
        key.FIELDS: list(VolunteerForm.__fields__),
    },
    f"{key.FORM}_ASK_QUESTION": {
        key.BUTTON_TEXT: "Задать вопрос",
        key.DESCRIPTION: "Далее необходимо заполнить поля для вопроса",
        key.MODEL: AskQuestionForm,
        key.FIELDS: list(AskQuestionForm.__fields__),
    },
}
