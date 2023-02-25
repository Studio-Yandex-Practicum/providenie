from bot.constants import key

DONATION_MENU = {
    f"{key.DONATION}_REPORT": {
        key.BUTTON_TEXT: "Годовые отчёты",
        key.DESCRIPTION: "https://fond-providenie.ru/docs/"
    },
    f"{key.DONATION}_LINK": {
        key.BUTTON_TEXT: "Сделать пожертвование",
        key.DESCRIPTION: (
            "https://fond-providenie.ru/help-chidren/sdelat-pozhertovanie"
            "/sdelat-pozhertvovanie-s-bankovskoj-karty/"
        )
    },
}

ABOUT_MENU = {
    f"{key.ABOUT}_WHO_ARE_WE": {
        key.BUTTON_TEXT: "Кто мы?",
        key.DESCRIPTION: "https://telegra.ph/Kto-my-02-06"
    },
    f"{key.ABOUT}_PROBLEM_SOLVING": {
        key.BUTTON_TEXT: "Какую социальную проблему мы решаем?",
        key.DESCRIPTION: "https://telegra.ph/Kakuyu-socialnuyu-problemu-my-reshaem-02-06"
    },
    f"{key.ABOUT}_HOW_PROBLEM_SOLVING": {
        key.BUTTON_TEXT: "Как мы её решаем?",
        key.DESCRIPTION: "https://telegra.ph/Kak-my-eyo-reshaem-02-06"
    },
    f"{key.ABOUT}_LIFE_CHANGE": {
        key.BUTTON_TEXT: "Как мы меняем жизнь людей?",
        key.DESCRIPTION: "https://telegra.ph/Kak-my-menyaem-zhizn-lyudej-02-06"
    },
    f"{key.ABOUT}_WHAT_IS_DONE": {
        key.BUTTON_TEXT: "Что мы уже сделали?",
        key.DESCRIPTION: "https://telegra.ph/CHto-uzhe-sdelano-Kto-obrashchaetsya-za-pomoshchyu-02-06"
    },
    f"{key.ABOUT}_WHY_DONATION_NEED": {
        key.BUTTON_TEXT: "Зачем нужны пожертвования?",
        key.DESCRIPTION: "https://telegra.ph/Zachem-nuzhny-pozhertvovaniya-02-06"
    },
    f"{key.ABOUT}_ABOUT_SUCCESS": {
        key.BUTTON_TEXT: "История успеха",
        key.DESCRIPTION: ("https://youtu.be/n-hByd_oiIo\n"
                          "https://youtu.be/NG4QUO-hvCk\n"
                          "https://youtu.be/cAQayg_ZNok\n"
                          "https://youtu.be/26mYPRE4BQo\n"
                          "https://youtu.be/CINnVYp6hQI")
    },
}


SHARE_MENU = {
    f"{key.SHARE}_WEBPAGE": {
        key.BUTTON_TEXT: "Интернет сайт",
        key.DESCRIPTION: " на страницу в интернете",
        key.LINK: "https://fond-providenie.ru/"
    },
    f"{key.SHARE}_VK": {
        key.BUTTON_TEXT: "VK",
        key.DESCRIPTION: " на страницу ВКонтакте",
        key.LINK: "https://vk.com/fond_providenie"
    },
    f"{key.SHARE}_INSTA": {
        key.BUTTON_TEXT: "Instagram",
        key.DESCRIPTION: " на страницу в Instagram",
        key.LINK: "https://instagram.com/fond_providenie/"
    },
    f"{key.SHARE}_FACEBOOK": {
        key.BUTTON_TEXT: "Facebook",
        key.DESCRIPTION: " на страницу в Facebook",
        key.LINK: "https://www.facebook.com/fond.providenie/"
    },
    f"{key.SHARE}_CHAT": {
        key.BUTTON_TEXT: "Новостной канал в Телеграм",
        key.DESCRIPTION: " в чат",
        key.LINK: "https://t.me/providenie_fond"
    },
    f"{key.SHARE}_TELEGRAM": {
        key.BUTTON_TEXT: "Приглашение в чат бот",
        key.DESCRIPTION: " в чат бот",
        key.LINK: "https://fond-providenie.ru/"
    },
}
