"""Send emails. Falls back to logging if SMTP is not configured."""
import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from config import (
    API_BASE_URL,
    EMAIL_SMTP_HOST,
    EMAIL_SMTP_PASSWORD,
    EMAIL_SMTP_PORT,
    EMAIL_SMTP_USER,
)

logger = logging.getLogger(__name__)


def _can_send() -> bool:
    return bool(EMAIL_SMTP_HOST and EMAIL_SMTP_USER and EMAIL_SMTP_PASSWORD)


def send_email(to: str, subject: str, html_body: str) -> bool:
    """Send an email. Returns True on success, False on failure. Logs instead if SMTP not configured."""
    if not _can_send():
        logger.warning(
            "Email not sent (SMTP not configured). Set EMAIL_SMTP_HOST, EMAIL_SMTP_USER, EMAIL_SMTP_PASSWORD in .env. to=%s subject=%s",
            to, subject
        )
        return True  # treat as success for dev
    logger.info("Attempting to send email: to=%s subject=%s from=%s", to, subject, EMAIL_SMTP_USER)
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = EMAIL_SMTP_USER
        msg["To"] = to
        msg.attach(MIMEText(html_body, "html"))
        with smtplib.SMTP(EMAIL_SMTP_HOST, EMAIL_SMTP_PORT, timeout=30) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(EMAIL_SMTP_USER, EMAIL_SMTP_PASSWORD)
            server.sendmail(EMAIL_SMTP_USER, to, msg.as_string())
        logger.info("Email sent successfully: to=%s subject=%s", to, subject)
        return True
    except Exception as e:
        logger.error(
            "EMAIL SEND FAILED to %s: %s. Check: 1) Gmail App Password is correct, 2) 2-Step Verification is ON, 3) No firewall blocking port 587.",
            to, e, exc_info=True
        )
        return False


def send_consultant_booking_request(
    consultant_email: str,
    client_name: str,
    client_email: str,
    date_str: str,
    time_str: str,
    service: str,
    notes: str,
    confirm_token: str,
    decline_token: str,
) -> bool:
    """Email consultant with appointment request and Confirm/Decline links."""
    confirm_url = f"{API_BASE_URL}/confirm?token={confirm_token}"
    decline_url = f"{API_BASE_URL}/decline?token={decline_token}"
    subject = f"Заявка за консултация – {client_name} – {date_str} {time_str}"
    html = f"""
    <html>
    <body style="font-family: sans-serif; max-width: 560px;">
    <h2>Нова заявка за консултация</h2>
    <p><strong>Клиент:</strong> {client_name}</p>
    <p><strong>Имейл:</strong> {client_email}</p>
    <p><strong>Дата:</strong> {date_str}</p>
    <p><strong>Час:</strong> {time_str}</p>
    <p><strong>Услуга:</strong> {service or '—'}</p>
    <p><strong>Бележки:</strong> {notes or '—'}</p>
    <p style="margin-top: 24px;">
    <a href="{confirm_url}" style="background: #22c55e; color: white; padding: 10px 20px; text-decoration: none; border-radius: 8px; margin-right: 12px;">Потвърди</a>
    <a href="{decline_url}" style="background: #ef4444; color: white; padding: 10px 20px; text-decoration: none; border-radius: 8px;">Откажи</a>
    </p>
    </body>
    </html>
    """
    return send_email(consultant_email, subject, html)


def send_client_confirmation(
    client_email: str,
    client_name: str,
    date_str: str,
    time_str: str,
    consultant_name: str,
) -> bool:
    """Email client after consultant confirms."""
    subject = f"Потвърдена консултация – {date_str} {time_str}"
    html = f"""
    <html>
    <body style="font-family: sans-serif; max-width: 560px;">
    <h2>Вашата консултация е потвърдена</h2>
    <p>Здравейте, {client_name}!</p>
    <p>Вашата заявка за консултация е приета.</p>
    <p><strong>Дата:</strong> {date_str}</p>
    <p><strong>Час:</strong> {time_str}</p>
    <p><strong>Консултант:</strong> {consultant_name}</p>
    <p>Очакваме ви!</p>
    </body>
    </html>
    """
    return send_email(client_email, subject, html)


def send_client_decline(
    client_email: str,
    client_name: str,
    date_str: str,
    time_str: str,
    consultant_name: str,
) -> bool:
    """Email client after consultant declines."""
    subject = f"Отхвърлена заявка за консултация – {date_str} {time_str}"
    html = f"""
    <html>
    <body style="font-family: sans-serif; max-width: 560px;">
    <h2>Вашата заявка за консултация е отхвърлена</h2>
    <p>Здравейте, {client_name}!</p>
    <p>Съжаляваме, но вашата заявка за консултация не може да бъде приета.</p>
    <p><strong>Дата:</strong> {date_str}</p>
    <p><strong>Час:</strong> {time_str}</p>
    <p><strong>Консултант:</strong> {consultant_name}</p>
    <p>Можете да направите нова заявка за друг ден или с друг експерт.</p>
    </body>
    </html>
    """
    return send_email(client_email, subject, html)
