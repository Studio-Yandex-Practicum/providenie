from bot.constants import key
from bot.conversations.models import ChatAngelsForm


DONATION = {
    f"{key.OPTION}_REPORT": {
        key.BUTTON_TEXT: "Годовые отчёты",
        key.DESCRIPTION: "Здесь вы найдете отчетность Фонда",
        key.LINK: "https://fond-providenie.ru/docs/",
    },
    f"{key.OPTION}_LINK": {
        key.BUTTON_TEXT: "Сделать пожертвование",
        key.DESCRIPTION: (
            "По ссылке вы можете сделать пожертвование. "
            "Убедительно просим Вас подключить регулярный платеж в Фонд. "
            "Это очень важно. Спасибо!"
        ),
        key.LINK: (
            "https://fond-providenie.ru/help-chidren/sdelat-pozhertovanie"
            "/sdelat-pozhertvovanie-s-bankovskoj-karty/"
        ),
    },
}

ABOUT = {
    f"{key.OPTION}_ABOUT_SUCCESS": {
        key.BUTTON_TEXT: "Истории успеха",
        key.DESCRIPTION: (
            "https://youtu.be/n-hByd_oiIo\n"
            "https://youtu.be/NG4QUO-hvCk\n"
            "https://youtu.be/cAQayg_ZNok\n"
            "https://youtu.be/26mYPRE4BQo\n"
            "https://youtu.be/CINnVYp6hQI"
        ),
    },
}

CHAT = {
    f"{key.OPTION}_BABY": {
        key.NAME: "Дети, рожде‌нные раньше срока (от рождения до 1,5 лет)",
        key.BUTTON_TEXT: 'Недоношенные дети до 1,5 лет',
        key.DESCRIPTION: (
            "Чат для родителей детей, рожде‌нных раньше срока. "
            "Здесь оказывается информационная и психологическая помощь "
            "родителям по любым вопросам, связанным с недоношенными детьми "
            "младше 1,5 лет. Для вступления в чат Вам необходимо предоставить "
            "информацию для куратора."
        ),
    },
    f"{key.OPTION}_CHILD": {
        key.NAME: "Дети, рожде‌нные раньше срока (от 1,5 лет)",
        key.BUTTON_TEXT: "Недоношенные дети от 1,5 лет",
        key.DESCRIPTION: (
            "Чат для родителей детей, рожде‌нных раньше срока. "
            "Здесь оказывается информационная и психологическая помощь "
            "родителям по любым вопросам, связанным с недоношенными детьми "
            "старше 1,5 лет. Для вступления в чат Вам необходимо предоставить "
            "информацию для куратора."
        ),
    },
    f"{key.OPTION}_RETINOPATIA": {
        key.BUTTON_TEXT: "Дети с ретинопатией недоношенных",
        key.DESCRIPTION: (
            "Чат для родителей детей с ретинопатией. "
            "Для вступления в чат Вам необходимо "
            "предоставить информацию для куратора."
        ),
    },
    f"{key.OPTION}_RETINOPATIA_4_5": {
        key.BUTTON_TEXT: "Ретинопатия недоношенных 4-5 стадии",
        key.DESCRIPTION: (
            "Чат для родителей детей с ретинопатией недоношенных 4-5 стадии. "
            "Для вступления в чат Вам необходимо "
            "предоставить информацию для куратора."
        ),
    },
    f"{key.OPTION}_PROBLEMS": {
        key.NAME: "Дети с другими нарушениями зрения",
        key.BUTTON_TEXT: "Дети с другими нарушениями зрения",
        key.DESCRIPTION: (
            "Чат для родителей детей с различными "
            "офтальмологическими проблемами "
            "(включая косоглазие). Для вступления в чат Вам необходимо "
            "предоставить информацию для куратора."
        ),
    },
    f"{key.OPTION}_REHABILITATION": {
        key.BUTTON_TEXT: "Реабилитация зрения",
        key.DESCRIPTION: (
            "Чат для родителей детей, нуждающихся в реабилитации зрения. "
            "Для вступления в чат Вам необходимо "
            "предоставить информацию для куратора."
        ),
    },
    f"{key.OPTION}_SHUNTATA": {
        key.BUTTON_TEXT: "Шунтята",
        key.DESCRIPTION: (
            "Чат для родителей детей с шунтами. "
            "Для вступления в чат Вам необходимо "
            "предоставить информацию для куратора."
        ),
    },
    f"{key.OPTION}_TELEGRAM": {
        key.NAME: "Помощь детям с СА и КИ (дети с нарушениями слуха) ",
        key.BUTTON_TEXT: "Помощь детям с нарушениями слуха",
        key.DESCRIPTION: (
            "Чат для родителей детей со слуховыми аппаратами и кохлеарной "
            "имплантацией. В чате обсуждаются вопросы, связанные с "
            "реабилитацией детей. Для вступления в чат Вам необходимо "
            "предоставить информацию для куратора."
        ),
    },
    f"{key.OPTION}_GRANDMOTHERS": {
        key.BUTTON_TEXT: "Бабушки недоношенных детей",
        key.DESCRIPTION: (
            "Чат для бабушек. Бабушки хотят помочь своим детям, "
            "внукам, но не знают как. При этом, сами нуждаются в поддержке! "
            "Именно поэтому, создана группа взаимной поддержки "
            "бабушек недоношенных детей. "
            "Для вступления в чат Вам необходимо "
            "предоставить информацию для куратора."
        ),
    },
    f"{key.OPTION}_CRY": {
        key.NAME: "Психологическая помощь мамам недоношенных детей",
        key.BUTTON_TEXT: "Психологическая помощь мамам",
        key.DESCRIPTION: (
            "Иногда очень хочется пожаловаться и поплакать. "
            "Ведь вокруг так много несправедливости! "
            "Чат психологической направленности. "
            "В чате всегда готовы помочь Вам профессиональные психологи и, "
            "конечно, мамы. "
            "Для вступления в чат Вам необходимо "
            "предоставить информацию для куратора."
        ),
    },
    f"{key.OPTION}_ANGELS": {
        key.BUTTON_TEXT: "Мамы ангелов",
        key.DESCRIPTION: (
            "Чат для родителей, которые столкнулись со смертью ребенка. "
            "Для вступления в чат Вам необходимо "
            "предоставить свое имя и телефон."
        ),
        key.CUSTOM_MODEL: ChatAngelsForm,
    },
}

FUND = {
    f"{key.OPTION}_LOOKWORLD": {
        key.NAME: "Смотри на мир (помощь детям с нарушениями зрения)",
        key.BUTTON_TEXT: "Смотри на мир (помощь детям с нарушениями зрения)",
        key.DESCRIPTION: (
            "Проект «Смотри на мир: СТОП ретинопатии недоношенных» "
            "нацелен на спасение зрения ребёнка "
            "и представляет собой своевременную информационную "
            "и психологическую поддержку всей семьи."
        ),
    },
    f"{key.OPTION}_REHABILITATION": {
        key.NAME: "Реабилитация недоношенных детей с инвалидностью",
        key.BUTTON_TEXT: "Реабилитация недоношенных детей с инвалидностью",
        key.DESCRIPTION: (
            "Детей, родившихся раньше срока, "
            "нередко сопровождают такие диагнозы, как дцп, тугоухость и т.д., "
            "что значительно осложняет жизнь им самим и их родителям. "
            "Вовремя проведенная реабилитация "
            "со специально подобранным комплексом процедур "
            "по современным методикам поможет "
            "значительно улучшить состояние ребёнка."
        ),
    },
    f"{key.OPTION}_LESSONS": {
        key.NAME: "Помощь незрячим и слабовидящим детям",
        key.BUTTON_TEXT: "Помощь незрячим и слабовидящим детям",
        key.DESCRIPTION: (
            "Помощь недоношенным детям с проблемами со зрением: "
            "трости для слепых детей, очки, линзы, "
            "лекарства для малоимущих семей из РФ и СНГ."
        ),
    },
    f"{key.OPTION}_PSYHELP": {
        key.NAME: "Психологическая поддержка семьи",
        key.BUTTON_TEXT: "Психологическая поддержка семьи",
        key.DESCRIPTION: (
            "Успех выхаживания и дальнейшее развитие недоношенного ребенка "
            "во многом зависят от грамотности и эмоциональной устойчивости "
            "родителей, граммотные психологи "
            "могут оказать в этом неоценимую поддержку."
        ),
    },
}
