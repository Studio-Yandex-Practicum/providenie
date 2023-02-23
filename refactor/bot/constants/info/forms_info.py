from bot.conversations.models import VolunteerForm, FundForm, ChatForm
from bot.constants.keys import FORM
from bot.constants.info.menus import FOND_MENU, CHAT_MENU

forms_info = {
    f"{FORM}_VOLONTEER": {
        "name": "Волонтерство",
        "desc": "Спасибо за интерес! Вам нужно будет предоставить информацию для куратора.",
        "button_text": "Стать волонтером",
        "model": VolunteerForm,
        "fields": list(VolunteerForm.__fields__),
    },
    f"{FORM}_FOND": {
        "name": "Заявка в фонд",
        "desc": "Выберите опцию:",
        "button_text": "Отправить заявку в фонд",
        "model": FundForm,
        "fields": list(FundForm.__fields__),
        "menu": FOND_MENU,
    },
    f"{FORM}_CHAT": {
        "name": "Родительский чат",
        "desc": "Выберите чат:",
        "button_text": "Попасть в родительский чат",
        "model": ChatForm,
        "fields": list(ChatForm.__fields__),
        'menu': CHAT_MENU,
    },
}