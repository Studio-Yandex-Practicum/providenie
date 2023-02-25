from bot.constants.info.form_menu import CHAT_MENU, FOND_MENU
from bot.constants.key import FORM
from bot.conversations.models import AskQuestionForm, ChatForm, FundForm, VolunteerForm

FORM_INFO = {
    f"{FORM}_CHAT": {
        "name": "Хочу попасть в родительский чат",
        "desc": "Выберите чат для вступления:",
        "model": ChatForm,
        "fields": list(ChatForm.__fields__),
        'menu': CHAT_MENU,
    },
    f"{FORM}_FOND": {
        "name": "Заявка в фонд",
        "desc": "Выберите программу фонда или вернитесь обратно в главное меню:",
        "model": FundForm,
        "fields": list(FundForm.__fields__),
        "menu": FOND_MENU,
    },
    f"{FORM}_VOLONTEER": {
        "name": "Хочу стать волонтёром",
        "desc": "Далее необходимо предоставить информацию для куратора",
        "model": VolunteerForm,
        "fields": list(VolunteerForm.__fields__),
    },
    f"{FORM}_ASK_QUESTION": {
        "name": "Задать вопрос",
        "desc": "Далее необходимо заполнить поля для вопроса",
        "model": AskQuestionForm,
        "fields": list(AskQuestionForm.__fields__),
    },
}
