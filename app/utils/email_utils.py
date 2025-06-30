import smtplib
import os
import mimetypes
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
SMTP_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("EMAIL_PORT", 465))

def send_email(to_email: str, subject: str, content: str, attachment_path: str = None) -> None:
    """
    Send an email with optional attachment.

    Args:
        to_email (str): Recipient email address.
        subject (str): Email subject line.
        content (str): Plain text content of the email.
        attachment_path (str, optional): Path to a file attachment. Defaults to None.

    Raises:
        Exception: If sending the email fails.
    """
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to_email
    msg.set_content(content)

    if attachment_path and os.path.isfile(attachment_path):
        with open(attachment_path, "rb") as f:
            file_data = f.read()
            file_name = os.path.basename(attachment_path)
            mime_type, _ = mimetypes.guess_type(file_name)
            maintype, subtype = (mime_type or "application/octet-stream").split("/")
            msg.add_attachment(file_data, maintype=maintype, subtype=subtype, filename=file_name)

    try:
        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
    except Exception as e:
        raise Exception(f"Failed to send email: {e}")
