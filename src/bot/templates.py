# Шаблоны для отправки куратору
from string import Template


HTML_TEMPLATE_JOIN_FOND = Template(
    """
    <html>
        <body>
            <h1>Тестовое письмо от пользователя: $mother_fio</h1>
            <h2>Данные пользователя:</h2>
            <p><b>Программа фонда:</b> $programm</p>
            <p><b>ФИО мамы:</b> $mother_fio</p>
            <p><b>Телефон мамы:</b> $mother_phone</p>
            <p><b>Email мамы:</b> $mother_email</p>
            <p><b>ФИО ребёнка:</b> $child_fio</p>
            <p><b>Членов семьи:</b> $how_many_people</p>
            <p><b>Город:</b> $city</p>
            <p><b>Адрес:</b> $adress</p>
            <p><b>Дата рождения ребёнка:</b> $child_date_birth</p>
            <p><b>Место рождения ребёнка:</b> $place_birth</p>
            <p><b>Срок рождения:</b> $spacing</p>
            <p><b>Вес ребёнка:</b> $weight</p>
            <p><b>Рост ребёнка:</b> $height</p>
            <p><b>Диагнозы:</b> $dizgnozes</p>
            <p><b>Дата обращения:</b> $date_aplication</p>
            <p><b>Как узнали о нас:</b> $how_about_us</p>
            <p><b>В каких фондах оформлены:</b> $fond_now</p>
            <p><b>Какие фонды помогали ранее:</b> $fond_early</p>
        </body>
    </html>"""
)


HTML_TEMPLATE_JOIN_FOND_ERROR = Template(
    """
    <html>
        <body>
            <h1>Ошибка</h1>
            <p><b>$error</b></p>
        </body>
    </html>"""
)
