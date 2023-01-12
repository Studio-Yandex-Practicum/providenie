import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from . import settings
from .logger import logger
from bot import constants as const


def bot_send_email_to_curator(subject: str, html: str) -> bool:
    """
    Отправка ботом сообщение на email куратору.
    Subject - тема сообщения.
    Html - тело письма в html формате.
    В месте, где будет вызываться данная функция
    нужно будет проверить истинность(True/False)
    для вывода пользователю об успехе отправки сообщения или
    же неудачной попытке.
    """
    smtp_server = None
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

        message.attach(MIMEText(html, "html"))

        smtp_server.send_message(message)
        logger.info(const.SUCCESSFUL_SENDING_MSG)

        return True

    except Exception as error:
        logger.error(const.ERROR_CANT_SEND_MSG_TO_EMAIL, error)
        return False

    finally:
        smtp_server.quit()
