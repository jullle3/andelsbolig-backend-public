import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from andelsbolig.advertisement.model import Advertisement
from andelsbolig.config.properties import GMAIL_PASSWORD
from andelsbolig.misc.logger import get_logger
from andelsbolig.notification.email import generate_email_content

logger = get_logger(__name__)
smtp_server = "smtp.gmail.com"
smtp_port = 587
gmail_user = "andelsboligbasen@gmail.com"
gmail_password = GMAIL_PASSWORD


def send_email(advertisement: Advertisement, to_email):
    msg = MIMEMultipart()
    msg["From"] = gmail_user
    msg["To"] = to_email
    msg["Subject"] = "Ny bolig fundet"

    # Attach the email body
    email_content = generate_email_content(advertisement)
    msg.attach(MIMEText(email_content, "html"))  # Use 'plain' for plain text emails

    # TODO: Bundle emails for efficiency
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(gmail_user, gmail_password)
            server.send_message(msg)
        logger.info(f"Email sent successfully to {to_email}")
    except Exception as e:
        logger.error(f"Failed to send email to {to_email}: {e}")
