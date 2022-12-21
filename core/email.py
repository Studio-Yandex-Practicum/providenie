import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from .logger import logger
from .settings import (
    PORT_SMTP_SERVER,
    SMTP_SERVER,
    EMAIL_BOT,
    EMAIL_BOT_PASSWORD,
    EMAIL_CURATOR
)


ERROR_CANT_SEND_MSG_TO_EMAIL = 'Неудается отправить сообщение на email куратора!'

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
# УБРАТЬ ТЕСТОВЫЕ ТЕМУ СООБЩЕНИЯ И ТЕКСТ. РАСКОММЕНТИТЬ subject, text_from_user
def bot_send_email_to_curator(subject: str, text_from_user: str):
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

        return True

    except Exception as error:
        logger.error(ERROR_CANT_SEND_MSG_TO_EMAIL, error)
        return False

    finally:
        smtp_server.quit()
