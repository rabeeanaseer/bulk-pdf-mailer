"""
email_sender.py
----------------
Sends an email with a PDF attachment using smtplib.

Works with any standard SMTP provider (Gmail, Outlook/Office365, Yahoo,
or a company mail server). For Gmail/Outlook you must use an "app password",
not your normal login password (see README.md).
"""

import smtplib
import ssl
from dataclasses import dataclass
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path


@dataclass
class SMTPConfig:
    host: str
    port: int
    username: str
    password: str
    use_tls: bool = True  # STARTTLS (port 587). Set False + use_ssl for port 465.
    use_ssl: bool = False


def send_email_with_attachment(
    smtp_config: SMTPConfig,
    to_email: str,
    subject: str,
    body: str,
    attachment_path: str,
    from_name: str = "",
) -> None:
    """
    Sends a single email with one PDF attachment.

    Raises an exception on failure so the caller can log/report it per-row
    instead of the whole batch silently failing.
    """
    msg = MIMEMultipart()
    from_display = f"{from_name} <{smtp_config.username}>" if from_name else smtp_config.username
    msg["From"] = from_display
    msg["To"] = to_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    attachment_path = Path(attachment_path)
    with open(attachment_path, "rb") as f:
        part = MIMEApplication(f.read(), _subtype="pdf")
        part.add_header(
            "Content-Disposition", "attachment", filename=attachment_path.name
        )
        msg.attach(part)

    if smtp_config.use_ssl:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_config.host, smtp_config.port, context=context) as server:
            server.login(smtp_config.username, smtp_config.password)
            server.sendmail(smtp_config.username, to_email, msg.as_string())
    else:
        with smtplib.SMTP(smtp_config.host, smtp_config.port) as server:
            if smtp_config.use_tls:
                server.starttls(context=ssl.create_default_context())
            server.login(smtp_config.username, smtp_config.password)
            server.sendmail(smtp_config.username, to_email, msg.as_string())
