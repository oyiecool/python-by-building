import smtplib, os
from email.message import EmailMessage

def send_alert(subject: str, body: str):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = os.environ["ALERT_FROM"]
    msg["To"] = os.environ["ALERT_TO"]
    msg.set_content(body)
    with smtplib.SMTP(os.environ.get("SMTP_HOST", "smtp.gmail.com"), 587) as s:
        s.starttls()
        s.login(os.environ["ALERT_FROM"], os.environ["SMTP_PASSWORD"])
        s.send_message(msg)
