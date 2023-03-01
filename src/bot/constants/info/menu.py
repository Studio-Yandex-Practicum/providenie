from bot.constants import key
from bot.constants.info import option, text
from bot.conversations.models import (AskQuestionForm, ChatForm, FundForm,
                                      VolunteerForm)


ALL_MENU = {
    f'{key.MENU}_CHAT': {
        key.BUTTON_TEXT: 'Хочу попасть в родительский чат',
        key.DESCRIPTION: 'Выберите чат для вступления:',
        key.MODEL: ChatForm,
        key.FIELDS: list(ChatForm.__fields__),
        key.OPTIONS: option.CHAT,
        key.RESPONSE: (
            'Спасибо за ваши ответы!'
            '\nВ течение 3 рабочих дней '
            'Вы получите приглашение в чат '
            'после рассмотрения заявки нашим куратором'
        ),
    },
    f'{key.MENU}_FOND': {
        key.BUTTON_TEXT: 'Заявка в фонд',
        key.DESCRIPTION: 'Выберите программу фонда:',
        key.MODEL: FundForm,
        key.FIELDS: list(FundForm.__fields__),
        key.OPTIONS: option.FUND,
        key.RESPONSE: (
            'Спасибо за ваши ответы!'
            '\nВаша заявка отправлена и скоро наш куратор свяжется с Вами '
            'в течение 7 рабочих дней.'
            '\nБудьте готовы отправить куратору следующие документы:'
            f'\n{text.REQUIRED_DOCUMENTS}'
        ),
    },
    f'{key.MENU}_VOLONTEER': {
        key.BUTTON_TEXT: 'Хочу стать волонтёром',
        key.DESCRIPTION:
            'Далее необходимо предоставить информацию для куратора',
        key.MODEL: VolunteerForm,
        key.FIELDS: list(VolunteerForm.__fields__),
        key.RESPONSE: (
            'Спасибо за ваши ответы!'
            '\nВаша заявка отправлена.'
            '\nТелефон для связи с координатором фонда + 79169814619 (Юлия)'
        ),
    },
    f'{key.MENU}_ASK_QUESTION': {
        key.BUTTON_TEXT: 'Задать вопрос',
        key.DESCRIPTION: 'Далее необходимо заполнить поля для вопроса',
        key.MODEL: AskQuestionForm,
        key.FIELDS: list(AskQuestionForm.__fields__),
        key.RESPONSE: (
            'Ваш вопрос успешно отправлен!'
            '\nНаш куратор свяжется с Вами в течение 3 рабочих дней.'
        ),
    },
    f'{key.MENU}_SHARE': {
        key.BUTTON_TEXT: 'Рассказать о Фонде своим друзьям',
        key.DESCRIPTION: 'Выберите интересующую вас соцсеть/страницу',
        key.OPTIONS: option.SHARE,
    },
    f'{key.MENU}_DONATION': {
        key.BUTTON_TEXT: 'Отчёты и пожертвование',
        key.DESCRIPTION: 'Сделать пожертвование',
        key.OPTIONS: option.DONATION,
    },
    f'{key.MENU}_EVENT': {
        key.BUTTON_TEXT: 'Наши события',
        key.DESCRIPTION: 'В разработке',
    },
    f'{key.MENU}_ABOUT': {
        key.BUTTON_TEXT: 'О Фонде',
        key.DESCRIPTION: 'Информация о фонде',
        key.OPTIONS: option.ABOUT,
    },
}
