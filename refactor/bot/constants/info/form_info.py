from bot.constants.info.form_menu import CHAT_MENU, FOND_MENU
from bot.constants.key import FORM
from bot.conversations.models import ChatForm, FundForm, VolunteerForm

SHOW_DATA_TEMPLATE = '<b><u>{title}</u></b>:\n\t\t{value}\n\n'
INPUT_ERROR_TEMPLATE = '<b>Некорректные введенные данные!</b>\n\n<b>Пример:</b> \n{hint}'
DATE_TEMPLATE = '%d.%m.%Y'

FORM_INFO = {
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