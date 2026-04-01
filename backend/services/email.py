import logging
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import aiosmtplib
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
OWNER_EMAIL = os.getenv("OWNER_EMAIL", "")
BUSINESS_EMAIL = os.getenv("BUSINESS_EMAIL", "")

BUSINESS_NAME = "GenHome"
BUSINESS_PHONE = os.getenv("OWNER_PHONE", "")

ACCENT = "#c8890a"

_BASE_STYLE = f"""
<style>
  body {{ font-family: Arial, sans-serif; background: #f4f4f4; margin: 0; padding: 0; }}
  .wrapper {{ max-width: 600px; margin: 30px auto; background: #ffffff; border-radius: 6px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
  .header {{ background: {ACCENT}; padding: 24px 32px; }}
  .header h1 {{ color: #ffffff; margin: 0; font-size: 22px; }}
  .body {{ padding: 28px 32px; color: #333333; line-height: 1.6; }}
  .body h2 {{ color: {ACCENT}; font-size: 16px; margin-top: 0; }}
  table {{ width: 100%; border-collapse: collapse; margin: 16px 0; }}
  td {{ padding: 8px 12px; border-bottom: 1px solid #eeeeee; font-size: 14px; }}
  td:first-child {{ font-weight: bold; width: 38%; color: #555555; }}
  .footer {{ background: #f9f9f9; padding: 16px 32px; font-size: 12px; color: #888888; border-top: 1px solid #eeeeee; }}
</style>
"""


def _row(label: str, value) -> str:
    value = value if value not in (None, "", "None") else "—"
    return f"<tr><td>{label}</td><td>{value}</td></tr>"


async def send_customer_confirmation(booking: dict) -> None:
    first_name = booking.get("first_name", "Valued Customer")
    html = f"""<!DOCTYPE html>
<html>
<head>{_BASE_STYLE}</head>
<body>
<div class="wrapper">
  <div class="header"><h1>{BUSINESS_NAME}</h1></div>
  <div class="body">
    <h2>Booking Request Received</h2>
    <p>Hi {first_name},</p>
    <p>Thank you for reaching out! We've received your booking request and will contact you
    within a few hours to confirm your appointment.</p>

    <h2>Your Booking Summary</h2>
    <table>
      {_row("Service", booking.get("service"))}
      {_row("Preferred Date", booking.get("preferred_date"))}
      {_row("Generator Size", booking.get("generator_size"))}
      {_row("Additional Details", booking.get("details"))}
    </table>

    <p>For urgent needs, please call us directly at <strong>{BUSINESS_PHONE}</strong>.</p>
    <p>We look forward to serving you!</p>
  </div>
  <div class="footer">
    {BUSINESS_NAME} &nbsp;|&nbsp; {BUSINESS_EMAIL} &nbsp;|&nbsp; {BUSINESS_PHONE}
  </div>
</div>
</body>
</html>"""

    subject = f"Booking Request Received — {BUSINESS_NAME}"
    to_email = booking.get("email", "")
    await _send(to_email, subject, html)


async def send_owner_notification(booking: dict) -> None:
    first = booking.get("first_name", "")
    last = booking.get("last_name", "")
    submitted_at = booking.get("created_at", "N/A")

    html = f"""<!DOCTYPE html>
<html>
<head>{_BASE_STYLE}</head>
<body>
<div class="wrapper">
  <div class="header"><h1>New Booking Received</h1></div>
  <div class="body">
    <h2>Customer Details</h2>
    <table>
      {_row("Name", f"{first} {last}")}
      {_row("Phone", booking.get("phone"))}
      {_row("Email", booking.get("email"))}
      {_row("Service", booking.get("service"))}
      {_row("Preferred Date", booking.get("preferred_date"))}
      {_row("Generator Size", booking.get("generator_size"))}
      {_row("Details", booking.get("details"))}
      {_row("Submitted At", submitted_at)}
    </table>
    <p>Log in to the admin panel to update the booking status and add notes.</p>
  </div>
  <div class="footer">
    {BUSINESS_NAME} &nbsp;|&nbsp; {BUSINESS_EMAIL} &nbsp;|&nbsp; {BUSINESS_PHONE}
  </div>
</div>
</body>
</html>"""

    subject = f"New Booking Request from {first} {last}"
    await _send(OWNER_EMAIL, subject, html)


async def send_order_customer_confirmation(order: dict) -> None:
    c = order.get("customer", {})
    first_name = c.get("first_name", "Valued Customer")
    items = order.get("items", [])
    total = order.get("total", 0)

    rows = "".join(
        f"<tr><td>{i.get('name', '')}</td><td>{i.get('kw', '')}kW — {i.get('fuel', '')}</td>"
        f"<td>x{i.get('quantity', 1)}</td><td>${i.get('unit_price', 0):,.0f}</td></tr>"
        for i in items
    )

    html = f"""<!DOCTYPE html>
<html>
<head>{_BASE_STYLE}</head>
<body>
<div class="wrapper">
  <div class="header"><h1>{BUSINESS_NAME}</h1></div>
  <div class="body">
    <h2>Order Received</h2>
    <p>Hi {first_name},</p>
    <p>Thank you for your order! We've received it and our team will contact you within a few hours
    to confirm availability and arrange payment.</p>

    <h2>Order Summary</h2>
    <table>
      <tr><td><strong>Product</strong></td><td><strong>Spec</strong></td><td><strong>Qty</strong></td><td><strong>Price</strong></td></tr>
      {rows}
    </table>
    <p><strong>Order Total: ${total:,.2f}</strong></p>

    <p>Payment details will be provided when we confirm your order. We accept bank transfer, Venmo, Chime, Apple Pay, and all major payment methods.</p>
    <p>For urgent needs, contact us at <strong>{BUSINESS_EMAIL}</strong>.</p>
  </div>
  <div class="footer">
    {BUSINESS_NAME} &nbsp;|&nbsp; {BUSINESS_EMAIL}
  </div>
</div>
</body>
</html>"""

    subject = f"Order Received — {BUSINESS_NAME}"
    to_email = c.get("email", "")
    await _send(to_email, subject, html)


async def send_order_owner_notification(order: dict) -> None:
    c = order.get("customer", {})
    items = order.get("items", [])
    total = order.get("total", 0)
    submitted_at = order.get("created_at", "N/A")

    rows = "".join(
        f"<tr><td>{i.get('name', '')}</td><td>{i.get('kw', '')}kW — {i.get('fuel', '')}</td>"
        f"<td>x{i.get('quantity', 1)}</td><td>${i.get('unit_price', 0):,.0f}</td></tr>"
        for i in items
    )

    html = f"""<!DOCTYPE html>
<html>
<head>{_BASE_STYLE}</head>
<body>
<div class="wrapper">
  <div class="header"><h1>New Order — {BUSINESS_NAME}</h1></div>
  <div class="body">
    <h2>Customer Details</h2>
    <table>
      {_row("Name", f"{c.get('first_name', '')} {c.get('last_name', '')}")}
      {_row("Phone", c.get("phone"))}
      {_row("Email", c.get("email"))}
      {_row("Company", c.get("company"))}
      {_row("Address", f"{c.get('address', '')} {c.get('city', '')} {c.get('state', '')} {c.get('zip', '')}")}
      {_row("Contact Preference", c.get("contact_pref"))}
      {_row("Best Time to Call", c.get("best_time"))}
      {_row("Notes", c.get("notes"))}
      {_row("Submitted At", submitted_at)}
    </table>

    <h2>Items Ordered</h2>
    <table>
      <tr><td><strong>Product</strong></td><td><strong>Spec</strong></td><td><strong>Qty</strong></td><td><strong>Price</strong></td></tr>
      {rows}
    </table>
    <p><strong>Order Total: ${total:,.2f}</strong></p>
    <p>Log in to the admin panel to manage this order.</p>
  </div>
  <div class="footer">
    {BUSINESS_NAME} &nbsp;|&nbsp; {BUSINESS_EMAIL}
  </div>
</div>
</body>
</html>"""

    subject = f"New Order from {c.get('first_name', '')} {c.get('last_name', '')}"
    await _send(OWNER_EMAIL, subject, html)


async def _send(to: str, subject: str, html: str) -> None:
    if not all([SMTP_USER, SMTP_PASSWORD, to]):
        logger.warning("Email not sent — missing SMTP credentials or recipient address.")
        return

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = f"{BUSINESS_NAME} <{SMTP_USER}>"
    msg["To"] = to
    msg.attach(MIMEText(html, "html"))

    try:
        await aiosmtplib.send(
            msg,
            hostname=SMTP_HOST,
            port=SMTP_PORT,
            username=SMTP_USER,
            password=SMTP_PASSWORD,
            start_tls=True,
        )
        logger.info("Email sent to %s: %s", to, subject)
    except Exception:
        logger.exception("Failed to send email to %s", to)
