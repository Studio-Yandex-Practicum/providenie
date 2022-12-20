import smtplib

# from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

################# После слива веток
# load_dotenv()

# EMAIL_BOT = os.getenv('EMAIL_BOT', 'FondProvidenieBot@yandex.ru')  # "providenie@yandex.ru"
# EMAIL_CURATOR = os.getenv('EMAIL_CURATOR', 'k.danilow2009@yandex.ru')
# EMAIL_BOT_PASSWORD = os.getenv('EMAIL_BOT_PASSWORD', 'w4Rj2_ESvsnKaZVu')

EMAIL_BOT = 'FondProvidenieBot@yandex.ru'
EMAIL_CURATOR = 'k.danilow2009@yandex.ru'
EMAIL_BOT_PASSWORD = 'w4Rj2_ESvsnKaZVu'

NAME_SENDER_EMAIL = 'Бот фонда "Провидение"'

# тестовый шаблон
html_context_testing = """\
    <html>
        <body>
            <h1>Тестовое письмо</h1>
        </body>
    </html>
"""


def bot_send_email_to_curator(subject: str, text_from_user: str):
    smtp_server = smtplib.SMTP('smtp.yandex.ru', 587)  # Ровнять по мылу бота
    smtp_server.starttls()

    message = MIMEMultipart()
    message['From'] = NAME_SENDER_EMAIL
    message['Subject'] = subject

    message.attach(MIMEText(text_from_user))
    message.attach(MIMEText(html_context_testing, 'html'))

    smtp_server.login(EMAIL_BOT, EMAIL_BOT_PASSWORD)

    smtp_server.sendmail(EMAIL_BOT, EMAIL_CURATOR, message.as_string())

# Далее вне контекста нужно разрешить небезопасные приложения на почте
