from bot.conversations.models import VolunteerForm, FundForm

volonteer_selections = {
    "FORM_VOLONTEER": {
        'desc': "Спасибо за интерес! Вам нужно будет предоставить информацию для куратора. TEST"
    }
}
fond_selections = {
    "SELECT_LOOKWORLD": {
        "name": "Смотри на мир",
        "desc": "111"
    },
    "SELECT_REHABILITATION": {
        "name": "Реабилитация",
        "desc": "222"
    },
    "SELECT_PSYHELP": {
        "name": "Психологическая помощь",
        "desc": "333"
    },
    "SELECT_LESSONS": {
        "name": "Уроки.",
        "desc": "444"
    },
}

forms = {
    "FORM_VOLONTEER": {
        "enry_button_text": "Стать волонтером",
        "schema": VolunteerForm,
        "selections": volonteer_selections
    },
    "FORM_FOND": {
        "enry_button_text": "Отправить заявку в фонд.",
        "schema": FundForm,
        "selections": fond_selections
    }
}