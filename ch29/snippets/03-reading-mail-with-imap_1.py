import email
import imaplib
import os
from email.header import decode_header, make_header

with imaplib.IMAP4_SSL("imap.gmail.com") as box:
    box.login(os.environ["SMTP_USER"], os.environ["SMTP_PASSWORD"])
    box.select("INBOX", readonly=True)                 # readonly: do not mark as read
    status, data = box.search(None, '(UNSEEN SUBJECT "invoice")')
    for num in data[0].split()[-10:]:                  # the 10 newest matches
        status, parts = box.fetch(num, "(RFC822)")
        msg = email.message_from_bytes(parts[0][1])
        subject = str(make_header(decode_header(msg["Subject"] or "")))
        print(msg["Date"], "|", msg["From"], "|", subject)
        for part in msg.walk():
            name = part.get_filename()
            if name and name.lower().endswith(".pdf"):
                with open(name, "wb") as f:            # save PDF attachments
                    f.write(part.get_payload(decode=True))
