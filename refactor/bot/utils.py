import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Optional

from telegram import InlineKeyboardButton as Button
from telegram import InlineKeyboardMarkup, Update

from bot.constants import key
from bot.constants.info.text import MAIL_SUBJECT, MESSAGE_MARKDOWN
from bot.core.settings import settings


async def send_message(
    update: Update,
    text: str,
    keyboard: Optional[InlineKeyboardMarkup] = None,
    link_preview: bool = False
):
    """Send a message with optional inline keyboard and link preview"""

    message_args = {
        'text': text,
        'reply_markup': keyboard,
        'parse_mode': MESSAGE_MARKDOWN,
        'disable_web_page_preview': not link_preview,
    }
    query = update.callback_query
    if query:
        await query.answer()
        await query.message.edit_text(**message_args)
    else:
        await update.message.reply_text(**message_args)


def get_menu_buttons(menu: dict):
    """Generate inline keyboard buttons for menu"""

    return [
        [Button(text=option.get(key.BUTTON_TEXT), callback_data=callback)]
        for callback, option in menu.items()
    ]


# Need refactoring
def send_email_message(message: str):
    msg = MIMEMultipart()
    msg['From'] = settings.smtp_server_bot_email
    msg['To'] = settings.email_curator
    msg['Subject'] = MAIL_SUBJECT
    msg.attach(MIMEText(message))
    try:
        mailserver = smtplib.SMTP(
            settings.smtp_server_address, settings.smtp_server_port
        )
        mailserver.ehlo()
        mailserver.starttls()
        mailserver.login(
            settings.smtp_server_bot_email, settings.smtp_server_bot_password
        )
        mailserver.set_debuglevel(1)  # for debugging
        mailserver.sendmail(
            settings.smtp_server_bot_email,
            settings.email_curator,
            msg.as_string()
        )
        mailserver.quit()
        logging.info("Письмо успешно отправлено")
    except smtplib.SMTPException:
        logging.error("Ошибка: Невозможно отправить почтовое сообщение")
