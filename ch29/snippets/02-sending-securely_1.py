import os, smtplib, ssl
from email.message import EmailMessage

msg = EmailMessage()
msg["Subject"] = "Backup finished"
msg["From"] = os.environ["SMTP_USER"]
msg["To"] = "ops@example.com"
msg.set_content("Nightly backup finished: 1,284 files, 0 errors.")

with smtplib.SMTP(os.environ.get("SMTP_HOST", "smtp.gmail.com"), 587, timeout=30) as smtp:
    smtp.starttls(context=ssl.create_default_context())   # encrypt before logging in
    smtp.login(os.environ["SMTP_USER"], os.environ["SMTP_PASSWORD"])
    smtp.send_message(msg)
