from bot.constants import key


SHORT_QUESTIONS = {
    'FULL_NAME': {
        key.TITLE: 'ФИО',
        key.TEXT: 'Введите фамилию, имя и отчество',
        key.HINT: 'Пример: Иванов Петр Сергеевич',
    },
    'PHONE': {
        key.TITLE: 'Номер телефона',
        key.TEXT: 'Введите свой контактный номер телефона',
        key.HINT: 'Пожалуйста, введите в формате 89xxxxxxxxx',
    },
    'EMAIL': {
        key.TITLE: 'Электронная почта',
        key.TEXT: 'Введите электронную почту',
        key.HINT: 'Пример: my_address@mail.ru',
    },
}

VOLUNTEER_QUESTIONS = {
    **SHORT_QUESTIONS,
    'BIRTHDAY': {
        key.TITLE: 'День рождения',
        key.TEXT: 'Введите дату своего рождения',
        key.HINT: 'Пожалуйста, введите в формате ДД.ММ.ГГГГ '
                  '(также возраст должен быть больше 18 лет)',
    },
    'CITY': {
        key.TITLE: 'Город',
        key.TEXT: 'Введите город проживания',
        key.HINT: 'Пример: Новосибирск',
    },
    'VOLUNTEER_HELP': {
        key.TITLE: 'Предлагаемая помощь',
        key.TEXT: 'Вы можете предложить свой вариант помощи',
        key.HINT: (
            'Пример: могу оказать помощь в транспортировке, '
            'есть машина легкового типа'
        ),
    },
}

ASK_QUESTIONS = {
    **SHORT_QUESTIONS,
    'QUESTION': {
        key.TITLE: 'Вопрос',
        key.TEXT: 'Введите Ваш вопрос',
        key.HINT: (
            'Пример: в какой фонд я могу обратиться, '
            'если моему ребенку нужна консультация офтальмолога?'
        ),
    },
}

LONG_QUESTIONS = {
    'PARENT_FULL_NAME': {
        key.TITLE: 'ФИО родителя',
        key.TEXT: 'Введите фамилию, имя и отчество родителя',
        key.HINT: 'Пример: Иванов Петр Сергеевич',
    },
    'PHONE': {
        key.TITLE: 'Номер телефона',
        key.TEXT: 'Введите свой контактный номер телефона',
        key.HINT: 'Пожалуйста, введите в формате 89xxxxxxxxx',
    },
    'EMAIL': {
        key.TITLE: 'Электронная почта',
        key.TEXT: 'Введите электронную почту',
        key.HINT: 'Пример: my_address@mail.ru',
    },
    'FAMILY_MEMBERS': {
        key.TITLE: 'Количество членов семьи',
        key.TEXT: 'Введите количество членов семьи',
        key.HINT: 'Пожалуйста, введите кол-во одной цифрой, например: 2',
    },
    'CITY': {
        key.TITLE: 'Город',
        key.TEXT: 'Введите город проживания',
        key.HINT: 'Пример: Ростов',
    },
    'CHILD_FULL_NAME': {
        key.TITLE: 'ФИО ребенка',
        key.TEXT: 'Введите фамилию, имя и отчество ребенка',
        key.HINT: 'Пример: Иванов Олег Сергеевич',
    },
    'CHILD_BIRTHDAY': {
        key.TITLE: 'Дата рождения ребенка',
        key.TEXT: 'Введите дату рождения ребенка',
        key.HINT: 'Пожалуйста, введите в формате ДД.ММ.ГГГГ'
                  '\n(Возраст ребенка не должен быть больше 18 лет)',
    },
    'CHILD_BIRTH_PLACE': {
        key.TITLE: 'Место рождения ребенка',
        key.TEXT: 'Введите место рождения ребенка',
        key.HINT: 'Пример: Челябинск',
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
        key.TITLE: 'Рост ребенка при рождении',
        key.TEXT: 'Введите рост ребенка при рождении',
        key.HINT: 'Пожалуйста, введите рост в СМ, например: 40',
    },
    'CHILD_DIAGNOSIS': {
        key.TITLE: 'Диагнозы ребенка',
        key.TEXT: (
            'Введите диагнозы ребенка '
            '(через запятую при наличии нескольких)'
        ),
        key.HINT: 'Пример: тугоухость 2ой степени, косоглазие, нистагм',
    },
    'WHERE_GOT_INFO': {
        key.TITLE: 'Как узнали о фонде',
        key.TEXT: 'Как Вы узнали о фонде?',
        key.HINT: 'Пример: увидел информационный пост на Яндекс Дзен',
    },
}

CHAT_QUESTIONS = {
    **LONG_QUESTIONS,
    'ADDITIONAL_CHATS': {
        key.TITLE: 'Дополнительные чаты',
        key.TEXT: 'В какие ещё чаты Вы хотели бы вступить?',
        key.HINT: 'Пример: Да, хочу вступить в \"Смотри на мир\", \"Шунтята\"',
    },
}
CHAT_ANGELS_QUESTIONS = {
    **SHORT_QUESTIONS,
    'FAMILY_MEMBERS': {
        key.TITLE: 'Количество членов семьи',
        key.TEXT: 'Введите количество членов семьи',
        key.HINT: 'Пожалуйста, введите кол-во одной цифрой, например: 2',
    },
    'CITY': {
        key.TITLE: 'Город',
        key.TEXT: 'Введите город проживания',
        key.HINT: 'Пример: Ростов',
    },
    'WHERE_GOT_INFO': {
        key.TITLE: 'Как узнали о фонде',
        key.TEXT: 'Как Вы узнали о фонде?',
        key.HINT: 'Пример: увидел информационный пост на Яндекс Дзен',
    },
    'ADDITIONAL_CHATS': {
        key.TITLE: 'Дополнительные чаты',
        key.TEXT: 'В какие ещё чаты Вы хотели бы вступить?',
        key.HINT: 'Пример: Да, хочу вступить в "Смотри на мир", "Шунтята"',
    },
}

FUND_QUESTIONS = {
    **LONG_QUESTIONS,
    'ADDRESS': {
        key.TITLE: 'Адрес',
        key.TEXT: 'Введите адрес проживания',
        key.HINT: 'Пример: Ростов, ул. Моравского, д.6, кв. 1',
    },
    'REQUIRED_THERAPY': {
        key.TITLE: 'Требуемое лечение',
        key.TEXT: (
            'Какое лечение требуется и какая стоимость лечения?'
            '\nТакже можно указать ссылку '
            'на техническое средство реабилитации, '
            'которое необходимо приобрести'
        ),
        key.HINT: 'Пример: Шунтирование',
    },
    'REQUEST_GOAL': {
        key.TITLE: 'Цель обращения',
        key.TEXT: 'Опишите кратко вашу ситуацию с указанием цели обращения',
        key.HINT: 'Пример: Обратился по тому что ...',
    },
    'SOCIAL_NETWORKS': {
        key.TITLE: 'Cоциальные сети',
        key.TEXT: 'Введите cсылку на социальные сети',
        key.HINT: 'Пример: vk.com/fond_providenie"',
    },
    'PARENTS_WORK_PLACE': {
        key.TITLE: 'Место работы родителей',
        key.TEXT: 'Введите место работы родителей',
        key.HINT: 'Пример: ОАО "Рога и Копыта"',
    },
    'ANOTHER_FUND_MEMBER': {
        key.TITLE: 'Состоите ли в другом фонде',
        key.TEXT: (
            'Состоите ли вы в данный момент в каком-либо фонде? '
            'Если да, то напишите название фонда'
        ),
        key.HINT: 'Пример: Да, Фонд «Название Фонда»',
    },
    'ANOTHER_FUND_HELP': {
        key.TITLE: 'Помогали ли другие фонды',
        key.TEXT: 'Вам помогали фонды раньше? Если да, то какие?',
        key.HINT: (
            'Пример: Да, сбор денежных средств '
            'на операцию фондом «Название Фонда»'
        ),
    },
}

ALL_QUESTIONS = {
    **VOLUNTEER_QUESTIONS,
    **ASK_QUESTIONS,
    **CHAT_QUESTIONS,
    **FUND_QUESTIONS,
    **CHAT_ANGELS_QUESTIONS,
}
