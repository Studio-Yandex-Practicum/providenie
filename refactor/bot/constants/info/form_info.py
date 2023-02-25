from bot.constants.info.form_menu import CHAT_MENU, FOND_MENU
from bot.constants.key import FORM
from bot.conversations.models import ChatForm, FundForm, VolunteerForm

FORM_INFO = {
    f"{FORM}_VOLONTEER": {
        "name": "Волонтерство",
        "desc": "Спасибо за интерес! Вам нужно будет предоставить информацию для куратора.",
        "model": VolunteerForm,
        "fields": list(VolunteerForm.__fields__),
    },
    f"{FORM}_FOND": {
        "name": "Заявка в фонд",
        "desc": "Выберите опцию:",
        "model": FundForm,
        "fields": list(FundForm.__fields__),
        "menu": FOND_MENU,
    },
    f"{FORM}_CHAT": {
        "name": "Родительский чат",
        "desc": "Выберите чат:",
        "model": ChatForm,
        "fields": list(ChatForm.__fields__),
        'menu': CHAT_MENU,
    },
}
