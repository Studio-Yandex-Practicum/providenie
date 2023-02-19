import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from . import settings

html = """\
<html>
  <body>
    <p>
        The body of the email
    </p>
  </body>
</html>
"""

def send_email(subject: str, text: str):
    context = ssl.create_default_context()

    try:
        server = smtplib.SMTP(settings.SMTP_SERVER, settings.PORT_SMTP_SERVER)
        server.starttls(context=context)
        server.login(settings.EMAIL_BOT, settings.EMAIL_BOT_PASSWORD)

        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = settings.EMAIL_BOT
        message["To"] = settings.EMAIL_CURATOR

        message.attach(MIMEText(html, "html"))

        server.sendmail(settings.EMAIL_BOT, settings.EMAIL_CURATOR, message.as_string())
    except Exception as e:
        pass
    finally:
        server.quit()
