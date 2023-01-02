import smtplib
from email.message import EmailMessage
import ssl
from app.core.config import settings


class Mailer:
    def send_email(self, receiver_email: str, subject: str, email_template: str):
        sender_email = settings.SENDER_EMAIL
        password = settings.EMAIL_PASSWORD

        em = EmailMessage()
        em['From'] = sender_email
        em['To'] = receiver_email
        em['Subject'] = subject
        em.set_content(email_template)
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(sender_email, password)
            result = smtp.sendmail(
                sender_email, receiver_email, em.as_string())
            return result


auth_mailer = Mailer()
