import smtplib
from email.message import EmailMessage

from src.config import EMAIL_USER, EMAIL_PASS, DRY_RUN
from src.logger import logger

def send_email(to_email, subject, body):

    if DRY_RUN:
        print(f"[DRY RUN] Email to {to_email}")
        logger.info(f"DRY RUN email to {to_email}")
        return "DRY_RUN"

    try:

        msg = EmailMessage()

        msg["Subject"] = subject
        msg["From"] = EMAIL_USER
        msg["To"] = to_email

        msg.set_content(body)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:

            smtp.login(EMAIL_USER, EMAIL_PASS)

            smtp.send_message(msg)

        logger.info(f"SUCCESS: {to_email}")

        return "SUCCESS"

    except Exception as e:

        logger.error(f"FAILED: {to_email} - {e}")

        return "FAILED"