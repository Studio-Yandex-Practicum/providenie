import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from .logger import logger
from .settings import PORT_SMTP_SERVER, SMTP_SERVER


load_dotenv()

EMAIL_BOT = os.getenv('EMAIL_BOT', 'FondProvidenieBot@yandex.ru')

# ЗАМЕНИТЬ НА МЫЛО КУРАТОРА ФОНДА
EMAIL_CURATOR = os.getenv('EMAIL_CURATOR', 'k.danilow2009@yandex.ru')
EMAIL_BOT_PASSWORD = os.getenv('EMAIL_BOT_PASSWORD', 'jyvsejdjxyixsxkh')

ERROR_CANT_SAND_MSG_TO_EMAIL = 'Неудается отправить сообщение на email куратора!'


# тестовый шаблон. СДелай со мной что-нибудь.
HTML_TEMPLATE = """
    <html>
        <body>
            <h1>Тестовое письмо</h1>
            <p> Здесь должна быть какой-то интересны шаблон :)</p>
        </body>
    </html>
"""

# ИСПАРВЬ МЕНЯ, КАК ТОЛЬКО БОТ ОЖИВЕТ И ПОЛУЧИТ СООБЩЕНИЕ ОТ ПОЛЬЗОВАТЕЛЯ
def bot_send_email_to_curator(subject: str, text_from_user: str):
    """
    Отправка ботом сообщение на email куратору.
    Subject - тема сообщения.
    Text_from_user - сообщение пользователя.
    """
    try:
        smtp_server = smtplib.SMTP(SMTP_SERVER, PORT_SMTP_SERVER)
        smtp_server.starttls()

        message = MIMEMultipart()
        message['From'] = EMAIL_BOT
        message['To'] = EMAIL_CURATOR
        message['Subject'] = "Тестовая тема письма"
        # message['Subject'] = subject

        smtp_server.login(EMAIL_BOT, EMAIL_BOT_PASSWORD)

        message.attach(MIMEText("Текст вымышленного письма."))
        # message.attach(MIMEText(text_from_user))
        message.attach(MIMEText(HTML_TEMPLATE, 'html'))

        smtp_server.send_message(message)

    except Exception as error:
        logger.error(ERROR_CANT_SAND_MSG_TO_EMAIL, error)

    finally:
        smtp_server.quit()
