from bot.constants import key

COMMON_QUESTIONS = {
    'FULL_NAME': {
        key.TITLE: 'ФИО',
        key.TEXT: 'Введите фамилию, имя и отчество',
        key.HINT: ('Пример: Иванов Петр или '
                   'Иванов Петр Сергеевич'),
    },
    'PHONE': {
        key.TITLE: 'Номер телефона',
        key.TEXT: 'Номер телефона',
        key.HINT: 'Пожалуйста, введите в формате 89xxxxxxxxx',
    },
    'EMAIL': {
        key.TITLE: 'Электронная почта',
        key.TEXT: 'Электронная почта',
        key.HINT: 'Пример: my_address@mail.ru',
    },
    'CITY': {
        key.TITLE: 'Город',
        key.TEXT: 'Город проживания',
        key.HINT: 'Пример: Новосибирск',
    },
    'FAMILY_MEMBERS': {
        key.TITLE: 'Количество членов семьи',
        key.TEXT: 'Сколько членов семьи (полная/неполная)?',
        key.HINT: 'Пожалуйста, введите кол-во одной цифрой, например: 2',
    },
    'WHERE_GOT_INFO': {
        key.TITLE: 'Как узнали о Фонде',
        key.TEXT: 'Как Вы узнали о нашем Фонде?',
        key.HINT: 'Пример: увидел информационный пост на Яндекс Дзен',
    },
    'ADDITIONAL_CHATS': {
        key.TITLE: 'Дополнительные чаты',
        key.TEXT: 'В какие ещё чаты Вы хотели бы вступить?',
        key.HINT: 'Пример: Да, хочу вступить в "Смотри на мир", "Шунтята"',
    }
}

VOLUNTEER_QUESTIONS = {
    'BIRTHDAY': {
        key.TITLE: 'День рождения',
        key.TEXT: 'Введите дату своего рождения',
        key.HINT: 'Пожалуйста, введите в формате ДД.ММ.ГГГГ '
                  '(также возраст должен быть больше 18 лет)',
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
        key.TITLE: 'ФИО мамы',
        key.TEXT: 'ФИО мамы',
        key.HINT: ('Пример: Иванова Мария или '
                   'Иванова Мария Петровна'),
    },
    'CHILD_FULL_NAME': {
        key.TITLE: 'ФИО ребенка',
        key.TEXT: 'ФИО ребенка',
        key.HINT: ('Пример: Иванов Олег или '
                   'Иванов Олег Петрович'),
    },
    'CHILD_BIRTHDAY': {
        key.TITLE: 'Дата рождения ребенка',
        key.TEXT: 'Дата рождения ребенка',
        key.HINT: 'Пожалуйста, введите в формате ДД.ММ.ГГГГ'
                  '\n(Возраст ребенка не должен быть больше 18 лет)',
    },
    'CHILD_BIRTH_PLACE': {
        key.TITLE: 'Место рождения ребенка',
        key.TEXT: 'Место рождения ребенка',
        key.HINT: 'Пример: Челябинск',
    },
    'CHILD_BIRTH_DATE': {
        key.TITLE: 'Срок беременности при рождении ребенка',
        key.TEXT: 'На каком сроке родился ребенок (полных недель)?',
        key.HINT: 'Пожалуйста, введите срок в НЕДЕЛЯХ, например: 35',
    },
    'CHILD_BIRTH_WEIGHT': {
        key.TITLE: 'Вес ребенка при рождении',
        key.TEXT: 'Какой был вес ребенка при рождении?',
        key.HINT: 'Пожалуйста, введите вес в ГРАММАХ, например: 3000',
    },
    'CHILD_BIRTH_HEIGHT': {
        key.TITLE: 'Рост ребенка при рождении',
        key.TEXT: 'Какой был рост ребенка при рождении?',
        key.HINT: 'Пожалуйста, введите рост в СМ, например: 40',
    },
    'CHILD_DIAGNOSIS': {
        key.TITLE: 'Диагнозы ребенка',
        key.TEXT: (
            'Какие диагнозы на момент обращения?'
        ),
        key.HINT: 'Пример: тугоухость 2ой степени, косоглазие, нистагм',
    },

}

FUND_QUESTIONS = {
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
            'на операцию Фондом «Название Фонда»'
        ),
    },
}

ALL_QUESTIONS = {
    **COMMON_QUESTIONS,
    **VOLUNTEER_QUESTIONS,
    **ASK_QUESTIONS,
    **LONG_QUESTIONS,
    **FUND_QUESTIONS,
}
