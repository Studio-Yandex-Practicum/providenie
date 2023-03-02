from bot.constants import key
from bot.constants.info.text import REQUIRED_DOCUMENTS
from bot.conversations.models import ShortForm


DONATION = {
    f'{key.OPTION}_REPORT': {
        key.BUTTON_TEXT: 'Годовые отчёты',
        key.DESCRIPTION: 'Здесь вы найдете отчетность фонда',
        key.LINK: 'https://fond-providenie.ru/docs/',
    },
    f'{key.OPTION}_LINK': {
        key.BUTTON_TEXT: 'Сделать пожертвование',
        key.DESCRIPTION: 'По ссылке вы можете сделать пожертвование. Убедительно просим Вас подключить регулярный платеж в фонд. Это очень важно. Спасибо!',
        key.LINK: (
            'https://fond-providenie.ru/help-chidren/sdelat-pozhertovanie'
            '/sdelat-pozhertvovanie-s-bankovskoj-karty/'
        ),
    },
}

ABOUT = {
    f'{key.OPTION}_WHO_ARE_WE': {
        key.BUTTON_TEXT: 'Кто мы?',
        key.DESCRIPTION: (
            'Мы – Благотворительный Фонд, '
            'основанный родителями недоношенного ребенка в 2018 году.'
        ),
        key.LINK: 'https://telegra.ph/Kto-my-02-06',
    },
    f'{key.OPTION}_PROBLEM_SOLVING': {
        key.NAME: 'Какую социальную проблему мы решаем?',
        key.BUTTON_TEXT: 'Какую проблему мы решаем?',
        key.DESCRIPTION: 'Основная задача Фонда — сохранить зрение детей.',
        key.LINK:
            'https://telegra.ph/Kakuyu-socialnuyu-problemu-my-reshaem-02-06',
    },
    f'{key.OPTION}_HOW_PROBLEM_SOLVING': {
        key.BUTTON_TEXT: 'Как мы её решаем?',
        key.DESCRIPTION: (
            'Главное направление работы фонда - '
            'комплексное сопровождение детей с проблемами по офтальмологии, '
            'в первую очередь вызванных ретинопатией недоношенных.'
        ),
        key.LINK: 'https://telegra.ph/Kak-my-eyo-reshaem-02-06',
    },
    f'{key.OPTION}_LIFE_CHANGE': {
        key.BUTTON_TEXT: 'Как мы меняем жизнь людей?',
        key.DESCRIPTION: (
            'Благодаря нашей работе '
            'подопечные из любой точки России и стран СНГ '
            'могут попасть на операцию по зрению в день обращения, '
            'заручившись поддержкой Фонда'
        ),
        key.LINK: 'https://telegra.ph/Kak-my-menyaem-zhizn-lyudej-02-06',
    },
    f'{key.OPTION}_WHAT_IS_DONE': {
        key.BUTTON_TEXT: 'Что мы уже сделали?',
        key.DESCRIPTION: (
            'На данный момент благодаря нашему Фонду '
            'уже почти 350 детей '
            'получили операции по сохранению и улучшению зрения.'
        ),
        key.LINK: (
            'https://telegra.ph/'
            'CHto-uzhe-sdelano-Kto-obrashchaetsya-za-pomoshchyu-02-06'
        ),
    },
    f'{key.OPTION}_WHY_DONATION_NEED': {
        key.BUTTON_TEXT: 'Зачем нужны пожертвования?',
        key.DESCRIPTION: (
            'Пожертвования, особенно регулярные, '
            'пусть даже на небольшие суммы, '
            'помогут нам планировать нашу деятельность '
            'и дадут возможность брать на попечение больше детей.'
        ),
        key.LINK: 'https://telegra.ph/Zachem-nuzhny-pozhertvovaniya-02-06',
    },
    f'{key.OPTION}_ABOUT_SUCCESS': {
        key.BUTTON_TEXT: 'История успеха',
        key.DESCRIPTION: (
            'https://youtu.be/n-hByd_oiIo\n'
            'https://youtu.be/NG4QUO-hvCk\n'
            'https://youtu.be/cAQayg_ZNok\n'
            'https://youtu.be/26mYPRE4BQo\n'
            'https://youtu.be/CINnVYp6hQI'
        ),
    },
}


SHARE = {
    f'{key.OPTION}_WEBPAGE': {
        key.BUTTON_TEXT: 'Интернет сайт',
        key.DESCRIPTION: 'Сайт благотворительного фонда “Провидение”',
        key.LINK: 'https://fond-providenie.ru/',
    },
    f'{key.OPTION}_VK': {
        key.BUTTON_TEXT: 'VK',
        key.DESCRIPTION: 'Группа Вконтакте',
        key.LINK: 'https://vk.com/fond_providenie',
    },
    f'{key.OPTION}_INSTA': {
        key.BUTTON_TEXT: 'Instagram',
        key.DESCRIPTION: 'Наша страница в Instagram',
        key.LINK: 'https://instagram.com/fond_providenie/',
    },
    f'{key.OPTION}_FACEBOOK': {
        key.BUTTON_TEXT: 'Facebook',
        key.DESCRIPTION: 'Группа в Facebook',
        key.LINK: 'https://www.facebook.com/fond.providenie/',
    },
    f'{key.OPTION}_TELEGRAM': {
        key.BUTTON_TEXT: 'Новостной канал в Телеграм',
        key.DESCRIPTION: (
            'Наш новостной канал Telegram '
            'с информацией о последних событиях фонда'
        ),
        key.LINK: 'https://t.me/providenie_fond',
    },
    f'{key.OPTION}_DZEN': {
        key.BUTTON_TEXT: 'Yandex Dzen',
        key.DESCRIPTION: 'Наша страница на Яндекс.Дзен',
        key.LINK: 'https://t.me/providenie_fond',
    },
    f'{key.OPTION}_MAIL': {
        key.BUTTON_TEXT: 'Mail.ru',
        key.DESCRIPTION: 'Наша страница на Mail.ru',
        key.LINK: 'https://t.me/providenie_fond',
    },
    f'{key.OPTION}_YOUTUBE': {
        key.BUTTON_TEXT: 'Youtube ',
        key.DESCRIPTION: 'Наш канал на Youtube',
        key.LINK: 'https://youtube.com/channel/UC_co5lBatw_pA2DceKCqZfg',
    },
}


CHAT = {
    f'{key.OPTION}_BABY': {
        key.NAME: 'Дети, рожде‌нные раньше срока (до 1,5 лет)',
        key.BUTTON_TEXT: 'Недоношенные дети до 1,5 лет',
        key.DESCRIPTION: (
            'В группе для родителей детей, рожде‌нных раньше срока, '
            'информационная и психологическая помощь родителям по любым '
            'вопросам, связанным с недоношенными детьми младше 1,5 лет. '
            'Для вступления в чат Вам необходимо '
            'предоставить информацию для куратора.'
        ),
    },
    f'{key.OPTION}_CHILD': {
        key.NAME: 'Дети, рожде‌нные раньше срока (старше 1,5 лет)',
        key.BUTTON_TEXT: 'Недоношенные дети старше 1,5 лет',
        key.DESCRIPTION: (
            'В группе для родителей детей, рожде‌нных раньше срока, '
            'информационная и психологическая помощь родителям по любым '
            'вопросам, связанным с недоношенными детьми старше 1,5 лет. '
            'Для вступления в чат Вам необходимо '
            'предоставить информацию для куратора.'
        ),
    },
    f'{key.OPTION}_RETINOPATIA': {
        key.BUTTON_TEXT: 'Дети с ретинопатией',
        key.DESCRIPTION: (
            'Группа для родителей деток с ретинопатией. '
            'Для вступления в чат Вам необходимо '
            'предоставить информацию для куратора.'
        ),
    },
    f'{key.OPTION}_SHUNTATA': {
        key.BUTTON_TEXT: 'Шунтята',
        key.DESCRIPTION: (
            'Группа для родителей деток с шунтами'
            'Для вступления в чат Вам необходимо '
            'предоставить информацию для куратора.'
        ),
    },
    f'{key.OPTION}_GRANDMOTHERS': {
        key.BUTTON_TEXT: 'Бабушки торопыжек',
        key.DESCRIPTION: (
            'Группа для бабушек. Бабушки хотят помочь своим детям, '
            'внукам, но не знают как. При этом, сами нуждаются в поддержке! '
            'Именно поэтому, создана группа взаимной поддержки '
            'бабушек недоношенных детей. '
            'Для вступления в чат Вам необходимо '
            'предоставить информацию для куратора.'
        ),
    },
    f'{key.OPTION}_CRY': {
        key.BUTTON_TEXT: 'Отвести душу и поплакать',
        key.DESCRIPTION: (
            'Иногда очень хочется пожаловаться и поплакать. '
            'Ведь вокруг так много несправедливости! '
            'Чат психологической направленности. '
            'В чате всегда готовы помочь Вам профессиональные психологи и, '
            'конечно, мамы. '
            'Для вступления в чат Вам необходимо '
            'предоставить информацию для куратора.'
        ),
    },
    f'{key.OPTION}_ANGELS': {
        key.BUTTON_TEXT: 'Мамы ангелов',
        key.DESCRIPTION: (
            'Чат для родителей, которые столкнулись со смертью ребенка'
            'Для вступления в чат Вам необходимо '
            'предоставить свое имя и телефон.'
        ),
        key.CUSTOM_MODEL: ShortForm,
    },
    f'{key.OPTION}_RETINOPATIA_4_5': {
        key.BUTTON_TEXT: 'Ретинопатия недоношеных 4-5 стадии',
        key.DESCRIPTION: (
            'Чат для родителей детей с ретинопатией недоношенных 4-5 стадии. '
            'Для вступления в чат Вам необходимо '
            'предоставить информацию для куратора.'
        ),
    },
    f'{key.OPTION}_PROBLEMS': {
        key.NAME: 'Дети с офтальмологическими проблемами',
        key.BUTTON_TEXT: 'Дети с болезнями глаз',
        key.DESCRIPTION: (
            'Чат для родителей детей с различными '
            'офтальмологическими проблемами '
            '(включая косоглазие). Для вступления в чат Вам необходимо '
            'предоставить информацию для куратора.'
        ),
    },
    f'{key.OPTION}_REHABILITATION': {
        key.BUTTON_TEXT: 'Реабилитация зрения',
        key.DESCRIPTION: (
            'Чат для родителей детей, нуждающихся в реабилитации зрения'
            'Для вступления в чат Вам необходимо '
            'предоставить информацию для куратора.'
        ),
    },
    f'{key.OPTION}_TELEGRAM': {
        key.BUTTON_TEXT: 'Семьи торопыжек',
        key.DESCRIPTION: (
            'Группа поддержки в Телеграмм «Помощь семьям торопыжек» '
            't.me/toropizhki. '
            'Для вступления в группу Вам необходимо предоставить '
            'информацию для куратора.'
        ),
    },
}

FUND = {
    f'{key.OPTION}_LOOKWORLD': {
        key.NAME: 'Смотри на мир (помощь детям с нарушениями зрения)',
        key.BUTTON_TEXT: 'Смотри на мир',
        key.DESCRIPTION: (
            'Проект «Смотри на мир: СТОП ретинопатии недоношенных» '
            'нацелен на спасение зрения ребёнка '
            'и представляет собой своевременную информационную '
            'и психологическую поддержку всей семьи.'
            f'{REQUIRED_DOCUMENTS}'
        ),
    },
    f'{key.OPTION}_REHABILITATION': {
        key.NAME: 'Реабилитация недоношенных детей с инвалидностью',
        key.BUTTON_TEXT: 'Реабилитация',
        key.DESCRIPTION: (
            'Деток, родившихся раньше срока, '
            'нередко сопровождают такие диагнозы, как дцп, тугоухость и т.д., '
            'что значительно осложняет жизнь им самим и их родителям. '
            'Вовремя проведенная реабилитация '
            'со специально подобранным комплексом процедур '
            'по современным методикам поможет '
            'значительно улучшить состояние ребёнка.'
            f'{REQUIRED_DOCUMENTS}'
        ),
    },
    f'{key.OPTION}_PSYHELP': {
        key.NAME: 'Психологическая поддержка семьи',
        key.BUTTON_TEXT: 'Помощь психолога',
        key.DESCRIPTION: (
            'Успех выхаживания и дальнейшее развитие недоношенного ребенка '
            'во многом зависят от грамотности и эмоциональной устойчивости '
            'родителей, граммотные психологи '
            'могут оказать в этом неоценимую поддержку.'
            f'{REQUIRED_DOCUMENTS}'
        ),
    },
    f'{key.OPTION}_LESSONS': {
        key.NAME: 'Помощь незрячим и слабовидящим детям',
        key.BUTTON_TEXT: 'Добрые уроки',
        key.DESCRIPTION: (
            'Помощь недоношенным детям с проблемами со зрением: '
            'трости для слепых детей, очки, линзы, '
            'лекарства для малоимущих семей из РФ и СНГ.'
            f'{REQUIRED_DOCUMENTS}'
        ),
    },
}
