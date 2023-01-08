import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from string import Template

from . import settings
from .logger import logger


ERROR_CANT_SEND_MSG_TO_EMAIL = (
    "Неудается отправить сообщение на email куратора!"
)
ERROR_BAD_DATES_FROM_USER = "Полученные данные не совпадают с формой!"

SUCCESSFUL_SENDING_MSG = "Сообщение отправлено куратору."


HTML_TEMPLATE = Template(
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

HTML_BAD_DATES_TEMPLATE = Template(
    """"
    <html>
        <body>
            <h1>СЛОМАНЫЙ ШАБЛОН</h1>
            <h2>Требуется разобраться с несостыковкой ключей из словаря пользователя с шаблоном.</h2>
            <p>$error</p>
        </body>
    </html>"""
)


def bot_send_email_to_curator(subject: str, dict_from_user: dict[str, str]) -> bool:
    """
    Отправка ботом сообщение на email куратору.
    Subject - тема сообщения.
    Text_from_user - сообщение пользователя.
    В месте, где будет вызываться данная функция
    нужно будет проверить истинность(True/False)
    для вывода пользователю об успехе отправки сообщения или
    же неудачной попытке.
    """
    try:
        smtp_server = smtplib.SMTP(
            settings.SMTP_SERVER, settings.PORT_SMTP_SERVER
        )
        smtp_server.starttls()

        message = MIMEMultipart()
        message["From"] = settings.EMAIL_BOT
        message["To"] = settings.EMAIL_CURATOR
        message["Subject"] = subject

        smtp_server.login(settings.EMAIL_BOT, settings.EMAIL_BOT_PASSWORD)

        try:
            html_from_user = HTML_TEMPLATE.substitute(
                mother_fio = dict_from_user["ФИО мамы"],
                programm = dict_from_user["Программа фонда"],
                mother_phone = dict_from_user["Телефон"],
                mother_email = dict_from_user["Email"],
                child_fio = dict_from_user["ФИО ребёнка"],
                how_many_people = dict_from_user["Сколько членов семьи"],
                city = dict_from_user["Город"],
                adress = dict_from_user["Адрес"],
                child_date_birth = dict_from_user["Дата рождения ребёнка"],
                place_birth = dict_from_user["Место рождения ребёнка"],
                spacing = dict_from_user["Срок рождения ребёнка"],
                weight = dict_from_user["Вес"],
                height = dict_from_user["Рост"],
                dizgnozes = dict_from_user["Диагнозы"],
                date_aplication = dict_from_user["Дата обращения"],
                how_about_us = dict_from_user["Как узнали о нас"],
                fond_now = dict_from_user["В фонде сейчас"],
                fond_early = dict_from_user["Фонды помогали"],
            )
        except Exception as error:
            logger.error(ERROR_BAD_DATES_FROM_USER)
            html_from_user = HTML_BAD_DATES_TEMPLATE.substitute(error = error)


        message.attach(MIMEText(html_from_user, 'html'))
        smtp_server.send_message(message)
        logger.info(SUCCESSFUL_SENDING_MSG)

        return True

    except Exception as error:
        logger.error(ERROR_CANT_SEND_MSG_TO_EMAIL, error)
        return False

    finally:
        smtp_server.quit()
