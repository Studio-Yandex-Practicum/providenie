import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from . import settings
from .logger import logger


ERROR_CANT_SEND_MSG_TO_EMAIL = (
    "Неудается отправить сообщение на email куратора!"
)
SUCCESSFUL_SENDING_MSG = "Сообщение отправлено куратору."

# Исправится, скорее всего, на этапе сбора информации от пользователя и отправке куратору
HTML_TEMPLATE = """
    <html>
        <body>
            <h1>Тестовое письмо</h1>
            <p> Здесь должна быть какой-то интересны шаблон :)</p>
        </body>
    </html>
"""


def bot_send_email_to_curator(subject: str, text_from_user: str) -> bool:
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

        message.attach(MIMEText(text_from_user))
        message.attach(MIMEText(HTML_TEMPLATE, "html"))

        smtp_server.send_message(message)
        logger.info(SUCCESSFUL_SENDING_MSG)

        return True

    except Exception as error:
        logger.error(ERROR_CANT_SEND_MSG_TO_EMAIL, error)
        return False

    finally:
        smtp_server.quit()
