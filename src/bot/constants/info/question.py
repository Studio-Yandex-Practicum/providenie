from bot.constants import key


SHORT_QUESTIONS = {
    'FULL_NAME': {
        key.TITLE: 'ФИО',
        key.TEXT: 'Введите фамилию, имя и отчество',
        key.HINT: 'подсказка',
    },
    'PHONE': {
        key.TITLE: 'Номер телефона',
        key.TEXT: 'Введите свой контактный номер телефона',
        key.HINT: 'Пожалуйста, введите в формате 89xxxxxxxxx',
    },
    'EMAIL': {
        key.TITLE: 'Email',
        key.TEXT: 'Введите email',
        key.HINT: 'подсказка',
    },
}

VOLUNTEER_QUESTIONS = {
    **SHORT_QUESTIONS,
    'BIRTHDAY': {
        key.TITLE: 'День рождения',
        key.TEXT: 'Введите дату своего рождения',
        key.HINT: 'Пожалуйста, введите в формате ДД.ММ.ГГГГ',
    },
    'CITY': {
        key.TITLE: 'Город',
        key.TEXT: 'Введите город проживания',
        key.HINT: 'подсказка',
    },
    'VOLUNTEER_HELP': {
        key.TITLE: 'Предлагаемая помощь',
        key.TEXT: 'Вы можете предложить свой вариант помощи',
        key.HINT: 'подсказка',
    },
}

ASK_QUESTIONS = {
    **SHORT_QUESTIONS,
    'QUESTION': {
        key.TITLE: 'Вопрос',
        key.TEXT: 'Введите Ваш вопрос',
        key.HINT: 'подсказка',
    },
}

LONG_QUESTIONS = {
    'PARENT_FULL_NAME': {
        key.TITLE: 'ФИО родителя',
        key.TEXT: 'Введите фамилию, имя и отчество родителя',
        key.HINT: 'подсказка',
    },
    'PHONE': {
        key.TITLE: 'Номер телефона',
        key.TEXT: 'Введите свой контактный номер телефона',
        key.HINT: 'Пожалуйста, введите в формате 89xxxxxxxxx',
    },
    'CHILD_FULL_NAME': {
        key.TITLE: 'ФИО ребенка',
        key.TEXT: 'Введите фамилию, имя и отчество ребенка',
        key.HINT: 'подсказка',
    },
    'CHILD_BIRTHDAY': {
        key.TITLE: 'Дата рождения ребенка',
        key.TEXT: 'Введите дату рождения ребенка',
        key.HINT: 'Пожалуйста, введите в формате ДД.ММ.ГГГГ',
    },
    'CHILD_BIRTH_PLACE': {
        key.TITLE: 'Место рождения ребенка',
        key.TEXT: 'Введите место рождения ребенка',
        key.HINT: 'подсказка',
    },
    'CHILD_BIRTH_DATE': {
        key.TITLE: 'Срок беременности при рождении ребенка',
        key.TEXT: 'Введите срок беременности при рождении ребенка',
        key.HINT: 'Пожалуйста, введите срок в НЕДЕЛЯХ, например: 35',
    },
    'CHILD_BIRTH_WEIGHT': {
        key.TITLE: 'Вес ребенка при рождении',
        key.TEXT: 'Введите вес ребенка при рождении',
        key.HINT: 'Пожалуйста, введите вес в ГРАММАХ, например: 3000',
    },
    'CHILD_BIRTH_HEIGHT': {
        key.TITLE: 'Рост ребенка',
        key.TEXT: 'Введите рост ребенка при рождении',
        key.HINT: 'Пожалуйста, введите рост в СМ, например: 40',
    },
    'CHILD_DIAGNOSIS': {
        key.TITLE: 'Диагноз ребенка',
        key.TEXT: (
            'Введите диагнозы ребенка '
            '(через запятую при наличии нескольких)'
        ),
        key.HINT: 'подсказка',
    },
    'WHERE_GOT_INFO': {
        key.TITLE: 'Как узнали о фонде',
        key.TEXT: 'Как Вы узнали о фонде?',
        key.HINT: 'подсказка',
    },
}

CHAT_QUESTIONS = {
    **LONG_QUESTIONS,
    'OPERATION': {
        key.TITLE: 'Информацию об операциях',
        key.TEXT: 'Были ли проведены операции? Дата и место операций?',
        key.HINT: 'подсказка',
    },
}

FUND_QUESTIONS = {
    **LONG_QUESTIONS,
    'EMAIL': {
        key.TITLE: 'Email',
        key.TEXT: 'Введите email',
        key.HINT: 'подсказка',
    },
    'FAMILY_MEMBERS': {
        key.TITLE: 'Количество членов семьи',
        key.TEXT: 'Введите количество членов семьи',
        key.HINT: 'Пожалуйста, введите кол-во одной цифрой, например: 2',
    },
    'CITY': {
        key.TITLE: 'Город',
        key.TEXT: 'Введите город проживания',
        key.HINT: 'подсказка',
    },
    'ADDRESS': {
        key.TITLE: 'Адрес',
        key.TEXT: 'Введите адрес проживания',
        key.HINT: 'подсказка',
    },
    'ANOTHER_FUND_MEMBER': {
        key.TITLE: 'Состоите ли в другом фонде',
        key.TEXT: (
            'Состоите ли вы в данный момент в каком-либо фонде? '
            'Если да, то напишите название фонда'
        ),
        key.HINT: 'подсказка',
    },
    'ANOTHER_FUND_HELP': {
        key.TITLE: 'Помогали ли другие фонды',
        key.TEXT: 'Вам помогали фонды раньше? Если да, то какие?',
        key.HINT: 'подсказка',
    },
}

ALL_QUESTIONS = {
    **VOLUNTEER_QUESTIONS,
    **ASK_QUESTIONS,
    **CHAT_QUESTIONS,
    **FUND_QUESTIONS,
}
