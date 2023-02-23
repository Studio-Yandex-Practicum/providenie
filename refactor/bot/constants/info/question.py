# Это как пример
# VOLONTEER_QUESTIONS = [
#     'VOLONTER_INFO_FIO',
#     'VOLONTER_INFO_BIRTHDAY',
#     'CITY',
#     'PHONE',
#     'EMAIL',
#     'VOLONTER_INFO_HELP'
# ]

# BASE = [
#     'PARENT_FULL_NAME',
#     'PHONE',
#     'CHILD_FULL_NAME',
#     'CHILD_BIRTHDAY',
#     'CHILD_BIRTH_DATE',
#     'CHILD_BIRTH_WEIGHT',
#     'CHILD_BIRTH_HEIGHT',
#     'CHILD_DIAGNOSIS',
#     'WHERE_GOT_INFO'
#     'REGIST_DATE',
# ]

# CHAT_QUESTIONS = [
#     *BASE,
#     'OPERATION',
#     'OPERATION_DATE',
#     'OPERATION_PLACE',
# ]

# FOND_QUESTIONS = [
#     *BASE,
#     'EMAIL',
#     'FAMILY_MEMBERS_NUM',
#     'CITY',
#     'ADDRESS',
# ]


ALL_QUESTIONS = {
    "FULL_NAME": {
        "name": "ФИО",
        "text": "Введите фамилию, имя и отчество",
        "hint": "подсказка",
    },
    "BIRTHDAY": {
        "name": "День рождения",
        "text": "Введите дату своего рождения",
        "hint": "подсказка",
    },
    "VOLUNTEER_HELP": {
        "name": "Предлагаемая помощь",
        "text": "Введите как вы можете нам помочь (не обязательно)",
        "hint": "подсказка",
    },
    "PARENT_FULL_NAME": {
        "name": "ФИО родителя",
        "text": "Введите фамилию, имя и отчество родителя",
        "hint": "подсказка",
    },
    "PHONE": {
        "name": "Номер телефона",
        "text": "Введите свой контактный номер телефона",
        "hint": "подсказка",
    },
    "CHILD_FULL_NAME": {
        "name": "ФИО ребенка",
        "text": "Введите фамилию, имя и отчество ребенка",
        "hint": "подсказка",
    },
    "CHILD_BIRTHDAY": {
        "name": "Дата рождения ребенка",
        "text": "Введите дату рождения ребенка",
        "hint": "подсказка",
    },
    "CHILD_BIRTH_DATE": {
        "name": "Срок рождения ребенка",
        "text": "Введите срок рождения ребенка",
        "hint": "подсказка",
    },
    "CHILD_BIRTH_WEIGHT": {
        "name": "Вес ребенка при рождении",
        "text": "Введите вес ребенка при рождении",
        "hint": "подсказка",
    },
    "CHILD_BIRTH_HEIGHT": {
        "name": "Рост ребенка",
        "text": "Введите рост ребенка при рождении",
        "hint": "подсказка",
    },
    "CHILD_DIAGNOSIS": {
        "name": "Диагноз ребенка",
        "text": "Введите диагноз ребенка",
        "hint": "подсказка",
    },
    "OPERATION": {
        "name": "Информацию об операции",
        "text": "Введите информацию о проведенной операции. Если операций не было введите \"нет\"",
        "hint": "подсказка",
    },
    "OPERATION_DATE": {
        "name": "Дата операции",
        "text": "Введите дату операции или введите \"нет\", если операции не проводилсь",
        "hint": "подсказка",
    },
    "OPERATION_PLACE": {
        "name": "Место операции",
        "text": "Введите место операции или введите \"нет\", если операции не проводилсь",
        "hint": "подсказка",
    },
    "REGIST_DATE": {
        "name": "Дата заполнения",
        "text": "Введите дату заполнения анкеты",
        "hint": "подсказка",
    },
    "WHERE_GOT_INFO": {
        "name": "Где узнали о фонде",
        "text": "Где вы узнали о фонде?",
        "hint": "подсказка",
    },
    "EMAIL": {
        "name": "Email",
        "text": "Введите email",
        "hint": "подсказка",
    },
    "FAMILY_MEMBERS": {
        "name": "Количество членов семьи",
        "text": "Введите количество членов семьи",
        "hint": "подсказка",
    },
    "CITY": {
        "name": "Город",
        "text": "Введите город проживания",
        "hint": "подсказка",
    },
    "ADDRESS": {
        "name": "Адрес",
        "text": "Введите адрес",
        "hint": "подсказка",
    },
}
