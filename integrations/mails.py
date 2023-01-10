import smtplib
import ssl
from app.core.config import settings
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class Mailer:
    def send_email(self, receiver_email: str, subject: str, email_content: str):
        sender_email = settings.SENDER_EMAIL
        password = settings.EMAIL_PASSWORD
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = receiver_email
        message['Subject'] = subject
        message.attach(MIMEText(email_content, "html"))
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(sender_email, password)
            result = smtp.sendmail(
                sender_email, receiver_email, message.as_string())
            return result


mailer = Mailer()
